import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient
from helpers import to_dict



class DeleteHandler(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            recipe = Recipe.get(self.request.get('key'))
            for qi in recipe.ingredients: qi.delete()
            recipe.delete()
        self.redirect('/')

    
