import os
import logging
from datetime import date

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
        thismonth = date.today().strftime("%B")

        query = Recipe.gql('WHERE %s = TRUE' % thismonth.lower())
        recipes = [r for r in query.fetch(10)]

        template_values = {
            'recipes' : recipes,
            'month' : thismonth,
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
