import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import images, users
from google.appengine.ext import db, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from models import Image, Recipe
from helpers import to_dict




################################################################################
class NewImageHandler(webapp.RequestHandler):
    # Returns JSON for the new image
    def post(self):
        imagedata = self.request.get('photofile')

        if not users.is_current_user_admin():
            return

        img = Image()
        # Note no recipe reference; this will come later
        img.data = db.Blob(imagedata)
        img.put()

        self.response.headers['Content-Type'] = 'text/javascript'
        self.response.out.write(simplejson.dumps({'key' : str(img.key())}))



################################################################################
class ImageHandler(webapp.RequestHandler):
    def get(self, key, size):
        img = Image.get(key)
        # TODO: cache resized images in blobstore
        data = images.resize(img.data, int(size))
        self.response.headers['Content-Type'] = 'image/png'
        self.response.headers['Cache-Control'] = 'max-age=7200'
        self.response.out.write(data)
