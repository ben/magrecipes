import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import images
from google.appengine.ext import db, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from models import Image, Recipe
from helpers import to_dict




################################################################################
class ImageHandler(webapp.RequestHandler):
    # Returns JSON for the new image
    def post(self, recipe_key):
        json_dict = {}

        recipe = Recipe.get(recipe_key)
        if (recipe != None):
            postedimage = self.request.FILES['photofile'].read()
            img = Image()
            img.full = db.Blob(postedimage)
            img.mid = db.Blob(images.resize(postedimage, 575))
            img.thumb = db.Blob(images.resize(postedimage, 200))

            json_dict = to_dict(img)

        self.response.headers['Content-Type'] = 'text/javascript'
        self.response.out.write(simplejson.dumps(json_dict))

    def get(self, recipe_key):
        # Returns JSON with size-indexed URLs for each of the recipe's images
        json_array = []

        recipe = Recipe.get(recipe_key)
        if (recipe != None):
            for img in recipe.images:
                json_array.append({
                        'full' : img.full,
                        'mid' : img.mid,
                        'thumb' : img.thumb,
                        })
        self.response.headers['Content-Type'] = 'text/javascript';
        self.response.out.write(simplejson.dumps(json_array))


################################################################################
class ImageBlobUpload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self, recipe_key):
        logging.debug("Uploading something...")
        try:
            for upload in self.get_uploads():
                logging.debug("It's an upload! " + upload.filename)
                upload.delete()
        except:
            pass
        return self.redirect("/")



            


################################################################################
class ImageBlobDownload(blobstore_handlers.BlobstoreDownloadHandler):
    pass
