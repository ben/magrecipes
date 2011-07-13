import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Recipe


################################################################################
class RecipesByTitleHandler(webapp.RequestHandler):
    def get(self):
        q = Recipe.all().order('title')
        recipes = [r for r in q]
        buckets = {}
        for r in recipes:
            key = r.title.lower()[:1]
            if not key in buckets:
                buckets[key] = []
            buckets[key].append(r)

        templatevalues = RequestContext(self.request, {
            'recipes' : recipes,
            'buckets' : buckets,
            })

        path = os.path.join(os.path.dirname(__file__), 'recipes_by_title.html')
        self.response.out.write(template.render(path, templatevalues))
        
