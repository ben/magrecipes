import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import Ingredient, Recipe

import markdown


################################################################################
class SearchHandler(webapp.RequestHandler):
    def post(self):
        # Search recipe bodies

        # Search ingredient names
        

        template_values = {
            'query' : self.request.get('q'),
            }
        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path, template_values))
