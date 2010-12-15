import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import Ingredient, Recipe

import markdown


################################################################################
class MainHandler(webapp.RequestHandler):
    def get(self):
        ingredients = Ingredient.all()
        recipes = Recipe.all()

        for r in recipes:
            r.instructions = markdown.markdown(r.instructions)

        template_values = {
            'ingredients' : ingredients,
            'recipes' : recipes,
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
