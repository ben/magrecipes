import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

from models import Ingredient, QuantifiedIngredient, Recipe

from helpers import allmonths



################################################################################
class NewRecipeHandler(webapp.RequestHandler):
    def property_to_bool(self, name):
        value = self.request.get(name)
        if value == 'on': return True
        return False

    def post(self):
        if not users.is_current_user_admin():
            return self.redirect('/')

        # Create a recipe
        therecipe = Recipe()

        # Values from request
        therecipe.title        = self.request.get('title')
        therecipe.instructions = self.request.get('instructions')
        therecipe.january      = self.property_to_bool('january')
        therecipe.february     = self.property_to_bool('february')
        therecipe.march        = self.property_to_bool('march')
        therecipe.april        = self.property_to_bool('april')
        therecipe.may          = self.property_to_bool('may')
        therecipe.june         = self.property_to_bool('june')
        therecipe.july         = self.property_to_bool('july')
        therecipe.august       = self.property_to_bool('august')
        therecipe.september    = self.property_to_bool('september')
        therecipe.october      = self.property_to_bool('october')
        therecipe.november     = self.property_to_bool('november')
        therecipe.december     = self.property_to_bool('december')

        # Save it so it has a key with which to associate
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
