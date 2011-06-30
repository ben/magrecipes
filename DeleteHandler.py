import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient, Sticky
from helpers import to_dict



class DeleteRecipeHandler(webapp.RequestHandler):
    def post(self):
        if not users.is_current_user_admin():
            return self.redirect(users.create_login_url(self.request.url))

        key = self.request.get('key')
        logging.debug("Deleting recipe " + key)
        recipe = Recipe.get(key)
        for qi in recipe.ingredients:
            logging.debug("Deleting QI " + str(qi.key()))
            qi.delete()
        recipe.delete()
        self.redirect('/')

    
class DeleteStickyHandler(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        logging.debug("Deleting sticky " + key)

        if not users.is_current_user_admin():
            return self.redirect(users.create_login_url(self.request.url))

        sticky = Sticky.get(key)
        sticky.delete()
        self.response.out.write("SUCCESS")
