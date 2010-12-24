#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required

from models import Ingredient, QuantifiedIngredient, Recipe

from MainHandler import MainHandler
from IngredientHandler import IngredientHandler
from NewRecipeHandler import NewRecipeHandler

# Custom template filters
template.register_template_library('templatefilters')


class DeleteAllHandler(webapp.RequestHandler):
    def get(self):
        if not users.is_current_user_admin():
            self.redirect('/')
        recipes = Recipe.all();
        for r in recipes:
            for i in r.ingredients:
                if i.ingredient: i.ingredient.delete()
                i.delete()
            r.delete()
        self.redirect('/')


################################################################################
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(
        [
            ('/', MainHandler),
            ('/addingredient', IngredientHandler),
            ('/newrecipe', NewRecipeHandler),
            #('/deleteall', DeleteAllHandler),
            ],
        debug=True)
    util.run_wsgi_app(application)
if __name__ == '__main__':
    main()
