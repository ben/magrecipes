import os
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.inclusion_tag(os.path.join(os.path.dirname(__file__), 'recipe_form.html'))
def recipe_form(json):
    return { 'json' : json }


@register.inclusion_tag(os.path.join(os.path.dirname(__file__), 'recipe_form.js'))
def recipe_viewmodel(json):
    return { 'json' : json }
