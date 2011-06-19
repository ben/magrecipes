#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')

import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, util
from google.appengine.ext.webapp import util

from models import Ingredient, QuantifiedIngredient, Recipe
from helpers import allmonths

# Handlers
from MainHandler import MainHandler
from NewRecipeHandler import NewRecipeHandler
from SearchHandler import SearchHandler
from ViewRecipeHandler import ViewRecipeHandler
from MonthHandler import MonthHandler
from DeleteHandler import DeleteHandler
from EditHandler import EditHandler

# Custom template filters
template.register_template_library('templatetags.recipe_summary')
template.register_template_library('templatetags.recipe_form')
template.register_template_library('templatetags.verbatim')
template.register_template_library('templatetags.ingredient_autocomplete')


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
        ('/delete', DeleteHandler),
        ('/edit/(.*)', EditHandler),
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
