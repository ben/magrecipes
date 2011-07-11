import os
import logging
from datetime import date

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient
from helpers import to_dict, allmonths

import markdown



def newMonthStruct(current, month):
    class expando(object): pass
    m = expando()
    m.full = month
    m.short = month[:3]
    m.shortlower = month[:3].lower()
    m.cls = ""
    if current == month: m.cls ="current"
    return m

################################################################################
class IndexHandler(webapp.RequestHandler):
    def get(self):
        thismonth = date.today().strftime("%B")
        months = [newMonthStruct(thismonth, m) for m in allmonths()]
        months[0].cls += " tl"
        months[-1].cls += " tr"
        

        query = Recipe.gql('WHERE %s = TRUE' % thismonth.lower())
        recipes = [r for r in query.fetch(10)]

        template_values = {
            'recipes' : recipes,
            'month' : thismonth,
            'months' : months,
            'is_admin' : users.is_current_user_admin(),
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
