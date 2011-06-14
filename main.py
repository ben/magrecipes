#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required

from models import Ingredient, QuantifiedIngredient, Recipe

# Handlers
from MainHandler import MainHandler
from NewRecipeHandler import NewRecipeHandler
from SearchHandler import SearchHandler

# Custom template filters
template.register_template_library('templatetags.recipe_summary')
template.register_template_library('templatetags.template_helpers')


class DeleteAllHandler(webapp.RequestHandler):
    def get(self):
        if not users.is_current_user_admin():
            self.redirect('/')
        recipes = Recipe.all()
        for qi in QuantifiedIngredient.all(): qi.delete()
        for i in Ingredient.all(): i.delete()
        for r in recipes: r.delete()
        self.redirect('/')


################################################################################
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(
        [
            ('/', MainHandler),
            ('/newrecipe', NewRecipeHandler),
            ('/search', SearchHandler),
            #('/deleteall', DeleteAllHandler),
            ],
        debug=True,
        )
    util.run_wsgi_app(application)
if __name__ == '__main__':
    main()
