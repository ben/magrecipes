import os
import logging
from datetime import date

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient
import helpers


################################################################################
class AboutHandler(webapp.RequestHandler):
    def get(self):
        template_values = RequestContext(self.request, {
            })
        path = os.path.join(os.path.dirname(__file__), 'about.html')
        self.response.out.write(template.render(path, template_values))
