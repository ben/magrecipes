#!/usr/bin/env python

import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from models import Ingredient, QuantifiedIngredient, Recipe

def RequiresLoggedIn(f):
    def callf(reqHandler, *args, **kwargs):
        if users.get_current_user():
            return f(reqHandler, *args, **kwargs)
        reqHandler.redirect(users.create_login_url(reqHandler.request.uri))
    return callf

class MainHandler(webapp.RequestHandler):

    #@RequiresLoggedIn
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        ingredients = Ingredient.all()
        quantifiedingredients = QuantifiedIngredient.all()

        template_values = {
            'url' : url,
            'url_linktext' : url_linktext,
            'ingredients' : ingredients,
            'quantifiedingredients' : quantifiedingredients,
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class IngredientHandler(webapp.RequestHandler):
    @RequiresLoggedIn
    def post(self):
        i = Ingredient()
        i.name = self.request.get('name')
        i.put()
        self.redirect('/')

class QuantifiedIngredientHandler(webapp.RequestHandler):
    @RequiresLoggedIn
    def post(self):
        qi = QuantifiedIngredient()
        qi.ingredient = Ingredient.get(self.request.get('ingredient'))
        qi.quantity = self.request.get('quantity')
        qi.put()
        self.redirect('/')

def main():
    application = webapp.WSGIApplication(
        [
            ('/', MainHandler),
            ('/addingredient', IngredientHandler),
            ('/addquantifiedingredient', QuantifiedIngredientHandler),
            ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
