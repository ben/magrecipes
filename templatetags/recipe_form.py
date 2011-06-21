import os, logging
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.inclusion_tag(os.path.join(os.path.dirname(__file__), 'recipe_form.html'))
def recipe_form(json, image_upload_url):
    return { 'json' : json, 'image_upload_url' : image_upload_url }


@register.inclusion_tag(os.path.join(os.path.dirname(__file__), 'recipe_form.js'))
def recipe_viewmodel(json):
    return { 'json' : json }
