import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import Ingredient, QuantifiedIngredient, Recipe



################################################################################
class RecipeHandler(webapp.RequestHandler):
    def post(self):
        if users.get_current_user():
            # Create a recipe
            recipe = Recipe()
            recipe.title = self.request.get('title')
            recipe.instructions = self.request.get('instructions')
            recipe.put()
            
            # Create the ingredients and associate them
            for i in xrange(1000):
                ingredientkey = self.request.get('ingredient' + str(i))
                if not ingredientkey: break
                ing = Ingredient.get(ingredientkey)
                if ing:
                    qi = QuantifiedIngredient()
                    qi.ingredient = ing
                    qi.quantity = self.request.get('amount' + str(i))
                    qi.note = self.request.get('note' + str(i))
                    qi.recipe = recipe
                    qi.put()
        self.redirect('/')
                

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'addrecipe.html')
        self.response.out.write(template.render(path, {}))
