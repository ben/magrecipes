import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

from models import Ingredient, QuantifiedIngredient, Recipe
from django.utils import simplejson

from helpers import allmonths, to_dict



################################################################################
class EditHandler(webapp.RequestHandler):

    def post(self, key):
        if not users.is_current_user_admin():
            return self.redirect('/')

        # Extract values from json
        json = simplejson.loads(self.request.get('json'))

        # Get the recipe
        r = Recipe.get(json['key'])
        if r == None:
            return self.redirect('/')

        # Modify recipe values and write
        r.title        = json['title']
        r.instructions = json['instructions']
        r.january      = bool(json['january'])
        r.february     = bool(json['february'])
        r.march        = bool(json['march'])
        r.april        = bool(json['april'])
        r.may          = bool(json['may'])
        r.june         = bool(json['june'])
        r.july         = bool(json['july'])
        r.august       = bool(json['august'])
        r.september    = bool(json['september'])
        r.october      = bool(json['october'])
        r.november     = bool(json['november'])
        r.december     = bool(json['december'])
        r.put()

        # Replace ingredients with new ones
        for qi in r.ingredients:
            qi.delete()
        for ivm in simplejson.loads(json['ingredients']):
            self.response.out.write(str(ivm) + "<br/>")
            ing = Ingredient.get_or_insert(ivm['name'],
                                           name=ivm['name'])
            qi = QuantifiedIngredient(ingredient=ing,
                                      quantity=ivm['quantity'],
                                      note=ivm['note'],
                                      recipe=r)
            qi.put()

        self.redirect("/recipe/" + str(r.key()))


    def get(self, key):
        if not users.is_current_user_admin():
            return self.redirect(users.create_login_url(self.request.url))

        recipe = Recipe.get(key)
        if (recipe == None):
            self.redirect('/')
            return

        recipe_dict = to_dict(recipe)
        recipe_dict['ingredients'] = [to_dict(i) for i in recipe.ingredients]
        recipe_dict['key'] = str(recipe.key())

        path = os.path.join(os.path.dirname(__file__), 'editrecipe.html')
        template_values = {
            'recipe' : recipe,
            'json' : simplejson.dumps(recipe_dict),
            'months' : allmonths(),
            }
        self.response.out.write(template.render(path, template_values))
