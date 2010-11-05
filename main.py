#!/usr/bin/env python

import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required

from models import Ingredient, QuantifiedIngredient, Recipe

class MainHandler(webapp.RequestHandler):

    #@login_required
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        ingredients = Ingredient.all()
        recipes = Recipe.all()

        template_values = {
            'url' : url,
            'url_linktext' : url_linktext,
            'ingredients' : ingredients,
            'ingredientrange' : range(3),
            'recipes' : recipes,
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class IngredientHandler(webapp.RequestHandler):
    def post(self):
        if users.get_current_user():
            i = Ingredient()
            i.name = self.request.get('name')
            i.put()
        self.redirect('/')

class RecipeHandler(webapp.RequestHandler):
    def post(self):
        if users.get_current_user():
            # Create a recipe
            recipe = Recipe()
            recipe.title = self.request.get('title')
            recipe.instructions = self.request.get('instructions')
            recipe.put()
            
            # Create the ingredients and associate them
            for i in xrange(1000):
                ingredientkey = self.request.get('ingredient' + str(i))
                if not ingredientkey: break
                ing = Ingredient.get(ingredientkey)
                if ing:
                    qi = QuantifiedIngredient()
                    qi.ingredient = ing
                    qi.quantity = self.request.get('amount' + str(i))
                    qi.note = self.request.get('note' + str(i))
                    qi.recipe = recipe
                    qi.put()
        self.redirect('/')
                

def main():
    application = webapp.WSGIApplication(
        [
            ('/', MainHandler),
            ('/addingredient', IngredientHandler),
            ('/addrecipe', RecipeHandler),
            ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
