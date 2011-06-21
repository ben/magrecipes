import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient
from helpers import to_dict

import markdown


def convert_to_dict(r):
    d = to_dict(r)
    d['key'] = str(r.key())
    d['ingredients'] = [i.ingredient.name for i in r.ingredients]
    return d

################################################################################
class IndexHandler(webapp.RequestHandler):
    def get(self):
        recipes = Recipe.all().fetch(10)
        recipe_dict = {'recipes': [convert_to_dict(r) for r in recipes]}
        for v in recipe_dict['recipes']:
            if v['title'] == '':
                v['title'] = '(no title)'

        template_values = {
            'json' : simplejson.dumps(recipe_dict),
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
