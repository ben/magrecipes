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

from models import Ingredient, QuantifiedIngredient, Recipe, Image
from helpers import allmonths, seasons

# Handlers
from IndexHandler import IndexHandler
from NewRecipeHandler import NewRecipeHandler
from SearchHandler import SearchHandler
from ViewRecipeHandler import ViewRecipeHandler
from MonthHandler import MonthHandler
from DeleteHandler import DeleteRecipeHandler, DeleteStickyHandler
from EditHandler import EditHandler
from ImageHandler import NewImageHandler, ImageHandler, RecipeImageHandler
from StickyHandler import StickyHandler

# Custom template filters
template.register_template_library('templatetags.recipe_summary')
template.register_template_library('templatetags.recipe_form')
template.register_template_library('templatetags.verbatim')
template.register_template_library('templatetags.ingredient_autocomplete')
template.register_template_library('templatetags.template_helpers')


class DeleteAllHandler(webapp.RequestHandler):
    def get(self):
        if not users.is_current_user_admin():
            self.redirect('/')
        for qi in QuantifiedIngredient.all(): qi.delete()
        for i in Ingredient.all(): i.delete()
        for r in Recipe.all(): r.delete()
        for img in Image.all(): img.delete()
        self.redirect('/')



################################################################################
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    mappings = [
        # Create
        ('/newrecipe', NewRecipeHandler),
        ('/image', NewImageHandler),
        ('/recipe/(.*)/images', RecipeImageHandler),
        ('/recipe/(.*)/stickies', StickyHandler),

        # Read
        ('/', IndexHandler),
        ('/search', SearchHandler),
        ('/recipe/(.*)', ViewRecipeHandler),
        ('/image/(.*)/(.*)', ImageHandler),

        # Update
        ('/edit/(.*)', EditHandler),

        # Delete
        ('/delete', DeleteRecipeHandler),
        ('/deletesticky', DeleteStickyHandler),
        #('/image/([^/]*)', ImageDeleteHandler),
        ####('/deleteall', DeleteAllHandler),
        ]

    # Month/season lists
    mappings.append(("/(" +
                     '|'.join(allmonths() + seasons().keys()) +
                     ")", MonthHandler))
    

    application = webapp.WSGIApplication(
        mappings,
        debug=True,
        )
    util.run_wsgi_app(application)
if __name__ == '__main__':
    main()
