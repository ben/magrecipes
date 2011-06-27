import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Recipe
from helpers import to_dict


class MonthHandler(webapp.RequestHandler):
    def get(self, month):
        recipes = [r for r in Recipe.gql('WHERE %s = TRUE' % month.lower())]

        templatevalues = {
            'month' : month.capitalize(),
            'recipes' : recipes,
            'json' : simplejson.dumps([r.to_dict() for r in recipes]),
            }

        path = os.path.join(os.path.dirname(__file__), 'month.html')
        self.response.out.write(template.render(path, templatevalues))


