import os, logging

from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Recipe
from helpers import to_dict, seasons


def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def queryForMonth(month):
    return GqlQuery('SELECT __key__ from Recipe WHERE %s = TRUE' % month.lower())

class MonthHandler(webapp.RequestHandler):
    def get(self, month):
        if month.capitalize() in seasons().keys():
            recipes = uniq([k for k in queryForMonth(seasons()[month][0])] +
                           [k for k in queryForMonth(seasons()[month][1])] +
                           [k for k in queryForMonth(seasons()[month][2])])
            recipes = [Recipe.get(k) for k in recipes]
        else:
            recipes = [r for r in Recipe.gql('WHERE %s = TRUE' % month.lower())]

        templatevalues = RequestContext(self.request, {
            'month' : month.capitalize(),
            'recipes' : recipes,
            'json' : simplejson.dumps([r.to_dict() for r in recipes]),
            })

        path = os.path.join(os.path.dirname(__file__), 'month.html')
        self.response.out.write(template.render(path, templatevalues))


