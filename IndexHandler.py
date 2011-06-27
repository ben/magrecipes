import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient
from helpers import to_dict

import markdown



################################################################################
class IndexHandler(webapp.RequestHandler):
    def get(self):
        recipes = [r for r in Recipe.all().fetch(10)]
        recipe_dict = {'recipes': [r.to_dict() for r in recipes]}
        for v in recipe_dict['recipes']:
            if v['title'] == '':
                v['title'] = '(no title)'

        template_values = {
            'recipes' : recipes,
            'json' : simplejson.dumps(recipe_dict),
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
