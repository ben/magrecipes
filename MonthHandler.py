import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Recipe
from helpers import to_dict


class MonthHandler(webapp.RequestHandler):
    def get(self, month):
        self.response.out.write(month)


