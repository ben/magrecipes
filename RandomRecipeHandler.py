import os
import random

from google.appengine.ext.db import Query
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Recipe


class RandomRecipeHandler(webapp.RequestHandler):
    def get(self):
        q = Query(Recipe, True)
        i = random.randint(0,q.count()-1)
        recipe = Recipe.get(q[i])
        if recipe == None:
            # TODO: error page?
            return

        recipe_dict = recipe.to_dict()

        templatevalues = RequestContext(self.request, {
            'recipe' : recipe,
            'json' : simplejson.dumps(recipe_dict),
            })

        path = os.path.join(os.path.dirname(__file__), 'randomrecipe.html')
        self.response.out.write(template.render(path, templatevalues))
