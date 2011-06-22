import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import images, users
from google.appengine.ext import db, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from models import Image, Recipe, ResizedImage
from helpers import to_dict


def SaveAndPackImage(response, data, recipe=None):
    img = Image()
    img.data = db.Blob(data)
    if (recipe != None): img.recipe = recipe
    img.put()

    response.headers['Content-Type'] = 'text/javascript'
    response.out.write(simplejson.dumps(img.to_dict()))


################################################################################
class NewImageHandler(webapp.RequestHandler):
    # Returns JSON for the new image
    def post(self):
        if users.is_current_user_admin():
            SaveAndPackImage(self.response, self.request.get('photofile'))



################################################################################
class ImageHandler(webapp.RequestHandler):
    def get(self, key, size):
        img = Image.get(key)

        # Cache resized images in blobstore
        
        query = img.sized_images.filter("size = ", int(size))
        logging.debug("Image: query for size '%s' has %d items" % (size, query.count()))
        if (query.count() == 0):
            # Store resized version
            data = images.resize(img.data, int(size))
            ri = ResizedImage()
            ri.data = db.Blob(data)
            ri.image = img
            ri.size = int(size)
            ri.put()
            self.response.out.write(data)
        else:
            # Return cached data
            self.response.out.write(query[0].data)
            
        self.response.headers['Content-Type'] = 'image/png'
        self.response.headers['Cache-Control'] = 'max-age=7200'



################################################################################
class RecipeImageHandler(webapp.RequestHandler):
    def post(self, recipe_key):
        recipe = Recipe.get(recipe_key)
        if users.is_current_user_admin() and recipe != None:
            SaveAndPackImage(self.response,
                             self.request.get('photofile'),
                             recipe)


