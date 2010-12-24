import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

from models import Ingredient, QuantifiedIngredient, Recipe

from helpers import allmonths



################################################################################
class NewRecipeHandler(webapp.RequestHandler):
    def post(self):
        if not users.is_current_user_admin():
            self.redirect('/')

        # Create a recipe
        therecipe = Recipe()
        therecipe.title = self.request.get('title')
        therecipe.instructions = self.request.get('instructions')
        therecipe.put()

        # Create the ingredients and associate them
        for i in xrange(1000):
            # Get the ingredient's name
            ingredient_name = self.request.get('ingredient' + str(i))
            if not ingredient_name: break

            # Fetch the ingredient, or create a new one.
            ing = Ingredient.get_or_insert(ingredient_name, name=ingredient_name)

            # Create QuantifiedIngredients for all the Ingredients in this recipe
            qi = QuantifiedIngredient(ingredient=ing,
                                      quantity = self.request.get('amount'+str(i)),
                                      note = self.request.get('note'+str(i)),
                                      recipe = therecipe)
            qi.put()

        self.redirect('/')
        

    def get(self):
        if not users.is_current_user_admin():
            return self.redirect(users.create_login_url('/newrecipe'))

        path = os.path.join(os.path.dirname(__file__), 'newrecipe.html')
        template_values = {
            'ingredients' : Ingredient.all(),
            'recipe' : Recipe(),
            'months' : allmonths(),
            }
        self.response.out.write(template.render(path, template_values))
