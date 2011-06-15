import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Recipe
from helpers import to_dict


class ViewRecipeHandler(webapp.RequestHandler):
    def get(self, recipekey):
        recipe = Recipe.get(recipekey)
        if recipe == None:
            # TODO: error page?
            return

        recipe_dict = to_dict(recipe)
        recipe_dict['ingredients'] = [to_dict(i) for i in recipe.ingredients]
        recipe_dict['key'] = str(recipe.key())

        templatevalues = {
            'title' : recipe.title,
            'json' : simplejson.dumps(recipe_dict),
            }

        path = os.path.join(os.path.dirname(__file__), 'viewrecipe.html')
        self.response.out.write(template.render(path, templatevalues))
