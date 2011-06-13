import os
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.inclusion_tag(os.path.join(os.path.dirname(__file__), 'recipe_summary.html'))
def summary(recipe):
    ingredients = [qi.ingredient.name for qi in recipe.ingredients]
    return { 'recipe': recipe,
             'ingredients' : ', '.join(ingredients),
             }


