import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Recipe, Ingredient, Tag
from helpers import allmonths

class NoTagsHandler(webapp.RequestHandler):
    def get(self):
        q = Recipe.all()

        templatevalues = RequestContext(self.request, {
                'recipes' : [r for r in q if len(r.tags) == 0]
                })

        path = os.path.join(os.path.dirname(__file__), 'no_tags.html')
        self.response.out.write(template.render(path, templatevalues))


################################################################################
class NoSeasonHandler(webapp.RequestHandler):
    def get(self):
        whereclause = ' AND '.join(['%s = FALSE' % m.lower()
                                    for m in allmonths()])
        logging.debug(whereclause)
        q = Recipe.gql('WHERE ' + whereclause)

        templatevalues = RequestContext(self.request, {
                'recipes' : [r for r in q]
                })

        path = os.path.join(os.path.dirname(__file__), 'no_season.html')
        self.response.out.write(template.render(path, templatevalues))
