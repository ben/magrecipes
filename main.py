#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required

from models import Ingredient, QuantifiedIngredient, Recipe
from helpers import allmonths

# Handlers
from MainHandler import MainHandler
from NewRecipeHandler import NewRecipeHandler
from SearchHandler import SearchHandler
from ViewRecipeHandler import ViewRecipeHandler
from MonthHandler import MonthHandler

# Custom template filters
template.register_template_library('templatetags.recipe_summary')
template.register_template_library('templatetags.verbatim')
template.register_template_library('templatetags.template_helpers')


class DeleteAllHandler(webapp.RequestHandler):
    def get(self):
        if not users.is_current_user_admin():
            self.redirect('/')
        for qi in QuantifiedIngredient.all(): qi.delete()
        for i in Ingredient.all(): i.delete()
        for r in Recipe.all(): r.delete()
        self.redirect('/')

    
################################################################################
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    mappings = [
        ('/', MainHandler),
        ('/newrecipe', NewRecipeHandler),
        ('/search', SearchHandler),
        ('/recipe/(.*)', ViewRecipeHandler),
        #('/deleteall', DeleteAllHandler),
        ]
    mappings.append(("/(" + '|'.join(allmonths()) + ")", MonthHandler))
    application = webapp.WSGIApplication(
        mappings,
        debug=True,
        )
    util.run_wsgi_app(application)
if __name__ == '__main__':
    main()
