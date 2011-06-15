from os import path
from google.appengine.ext import webapp
from models import Ingredient

register = webapp.template.create_template_register()

@register.inclusion_tag(path.join(path.dirname(__file__), 'ingredient_autocomplete.html'))
def ingredient_autocomplete():
    return { 'ingredients' : Ingredient.all() }
