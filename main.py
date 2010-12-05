#!/usr/bin/env python

import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required

from models import Ingredient, QuantifiedIngredient, Recipe

from MainHandler import MainHandler
from IngredientHandler import IngredientHandler
from RecipeHandler import RecipeHandler


################################################################################
def main():
    application = webapp.WSGIApplication(
        [
            ('/', MainHandler),
            ('/addingredient', IngredientHandler),
            ('/addrecipe', RecipeHandler),
            ],
                                         debug=True)
    util.run_wsgi_app(application)
if __name__ == '__main__':
    main()
