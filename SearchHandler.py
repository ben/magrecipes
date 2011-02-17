import os
import logging
import re

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import Ingredient, Recipe


################################################################################
class SearchHandler(webapp.RequestHandler):
    def post(self):
        query = self.request.get('q')
        ingredients = []
        recipes = []
        if query != '':
            # Pre-compile a regex for matching
            regex = re.compile(query, re.I)
            
            # Search ingredient names
            allingredients = Ingredient.all(keys_only=True)
            ingredients = [i.name() for i in allingredients
                           if regex.search(i.name())]
            
            # Search recipe bodies
            allrecipes = Recipe.all()
            recipes = [r for r in allrecipes
                       if (regex.search(r.title) or regex.search(r.instructions))]
        
        template_values = {
            'ingredients' : ingredients,
            'recipes' : recipes,
            'query' : query,
            }
        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path, template_values))
