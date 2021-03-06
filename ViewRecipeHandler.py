import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Recipe
from helpers import to_dict


class ViewRecipeHandler(webapp.RequestHandler):
    def get(self, recipekey):
        recipe = Recipe.get(recipekey)
        if recipe == None:
            # TODO: error page?
            return

        recipe_dict = recipe.to_dict()
        image = None
        if recipe.images.count(1) > 0: image = recipe.images[0].key()

        templatevalues = RequestContext(self.request, {
            'recipe' : recipe,
            'image' : image,
            'json' : simplejson.dumps(recipe_dict),
            })

        path = os.path.join(os.path.dirname(__file__), 'viewrecipe.html')
        self.response.out.write(template.render(path, templatevalues))
