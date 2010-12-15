import os

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

from models import Ingredient, QuantifiedIngredient, Recipe



################################################################################
class RecipeHandler(webapp.RequestHandler):
    def post(self):
        if not users.is_current_user_admin():
            self.redirect('/')

         # Create a recipe
        recipe = Recipe()
        recipe.title = self.request.get('title')
        recipe.instructions = self.request.get('instructions')
        recipe.put()

         # Create the ingredients and associate them
        for i in xrange(1000):
            # Get the ingredient's name
            ingredient_name = self.request.get('ingredient' + str(i))
            if not ingredient_name: break

             # Fetch the ingredient, or create a new one. This runs in a transaction
            ing_inst = Ingredient.all().filter('name =', ingredient_name).get()
            if ing_inst is None:
                ing_instance = Ingredient(name=ingredient_name)
                ing_instance.put()

            # Create QuantifiedIngredients for all the Ingredients in this recipe
            qi = QuantifiedIngredient(ingredient=ing_inst,
                                      quantity = self.request.get('amount'+str(i)),
                                      note = self.request.get('note'+str(i)),
                                      recipe = recipe)
            qi.put()

        self.redirect('/')
                

    def get(self):
        if not users.get_current_user():
            return self.redirect(users.create_login_url('/addrecipe'))

        path = os.path.join(os.path.dirname(__file__), 'addrecipe.html')
        self.response.out.write(template.render(path, {'ingrange':range(3)}))
