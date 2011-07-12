import os
import logging
from datetime import date

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Ingredient, Recipe, QuantifiedIngredient
import helpers

import markdown


class expando(object): pass

def newMonthStruct(month):
    thismonth = date.today().strftime("%B")
    m = expando()
    m.full = month
    m.short = month[:1]
    m.shortlower = month[:3].lower()
    m.cls = ""
    if thismonth == month: m.cls ="current"
    return m

def newSeasonStruct(name, extraCls, extraMonths):
    thismonth = date.today().strftime("%B")
    months = helpers.seasons()[name]
    s = expando()
    s.name = name
    s.cls = name.lower() + ' ' + extraCls
    if thismonth in months: s.cls += ' current'
    s.months = ','.join(["#%s" % m[:3] for m in months]) + ',' + extraMonths
    return s
    

################################################################################
class IndexHandler(webapp.RequestHandler):
    def get(self):
        months = [newMonthStruct(m) for m in helpers.allmonths()]
        months[0].cls += " tl"
        months[-1].cls += " tr"

        seasons = [
            newSeasonStruct('Winter', 'bl two-col', '.winter'),
            newSeasonStruct('Spring', 'three-col',  ''),
            newSeasonStruct('Summer', 'three-col',  ''),
            newSeasonStruct('Fall',   'three-col',  ''),
            newSeasonStruct('Winter', 'br one-col', '.winter'),
            ]
        
        template_values = RequestContext(self.request, {
            'months' : months,
            'seasons' : seasons,
            })
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
