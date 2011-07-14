import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp, db, blobstore
from google.appengine.ext.db import Key
from google.appengine.ext.webapp import template
from django.template.context import RequestContext

from models import Ingredient, QuantifiedIngredient, Recipe, Image

from django.utils import simplejson

from helpers import allmonths, to_dict



################################################################################
class NewRecipeHandler(webapp.RequestHandler):
    def property_to_bool(self, name):
        value = self.request.get(name)
        if value == 'on': return True
        return False

    def post(self):
        if not users.is_current_user_admin():
            return self.redirect('/')

        # Extract values from json
        json = simplejson.loads(self.request.get('json'))

        # Create a recipe
        therecipe = Recipe()
        therecipe.set_from_dict(json)

        self.redirect('/recipe/%s' % therecipe.key())
        

    def get(self):
        if not users.is_current_user_admin():
            return self.redirect(users.create_login_url(self.request.url))

        r = Recipe().to_dict()

        path = os.path.join(os.path.dirname(__file__), 'newrecipe.html')
        template_values = RequestContext(self.request, {
            'json' : simplejson.dumps(r),
            'image_upload_url' : '/image',
            })
        self.response.out.write(template.render(path, template_values))
