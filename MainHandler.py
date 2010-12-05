import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import Ingredient, Recipe



################################################################################
class MainHandler(webapp.RequestHandler):
    def get(self):
        ingredients = Ingredient.all()
        recipes = Recipe.all()

        template_values = {
            'ingredients' : ingredients,
            'ingredientrange' : range(3),
            'recipes' : recipes,
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
