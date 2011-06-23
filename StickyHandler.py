import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import images, users
from google.appengine.ext import db, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from models import Recipe, Sticky

class StickyHandler(webapp.RequestHandler):
    def post(self, recipe_key):
        recipe = Recipe.get(recipe_key)
        if users.is_current_user_admin() and recipe != None:
            sticky = Sticky()
            sticky.recipe = recipe
            sticky.text = self.request.get('text')
            sticky.put()

            self.response.headers['Content-Type'] = 'text/javascript'
            self.response.out.write(simplejson.dumps(sticky.to_dict()))


