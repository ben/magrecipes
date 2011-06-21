import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp, db, blobstore
from google.appengine.ext.webapp import template

from models import Ingredient, QuantifiedIngredient, Recipe
from django.utils import simplejson

from helpers import allmonths, to_dict



################################################################################
class EditHandler(webapp.RequestHandler):

    def get(self, key):
        if not users.is_current_user_admin():
            return self.redirect(users.create_login_url(self.request.url))

        recipe = Recipe.get(key)
        if (recipe == None):
            self.redirect('/')
            return

        recipe_dict = recipe.to_dict()
        recipe_dict['key'] = str(recipe.key())

        path = os.path.join(os.path.dirname(__file__), 'editrecipe.html')
        template_values = {
            'recipe' : recipe,
            'json' : simplejson.dumps(recipe_dict),
            }
        self.response.out.write(template.render(path, template_values))


    def post(self, key):
        if not users.is_current_user_admin():
            return self.redirect('/')

        # Extract values from json
        json = simplejson.loads(self.request.get('json'))

        # Get the recipe
        r = Recipe.get(json['key'])
        if r == None:
            return self.redirect('/')

        # Set the new values
        r.set_from_dict(json)

        self.redirect("/recipe/" + str(r.key()))


