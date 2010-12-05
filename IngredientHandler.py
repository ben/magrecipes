from google.appengine.ext import webapp
from google.appengine.api import users

from models import Ingredient


################################################################################
class IngredientHandler(webapp.RequestHandler):
    def post(self):
        if users.get_current_user():
            i = Ingredient()
            i.name = self.request.get('name')
            i.put()
        self.redirect('/')



