import os, logging
from google.appengine.ext import webapp
from os.path import join, dirname
from models import Tag

register = webapp.template.create_template_register()

@register.inclusion_tag(join(dirname(__file__), 'recipe_form.html'))
def recipe_form(json, image_upload_url):
    return { 'json' : json, 'image_upload_url' : image_upload_url }


@register.inclusion_tag(join(dirname(__file__), 'recipe_form.js'))
def recipe_viewmodel(json):
    return {
        'json' : json,
        'alltags' : [t for t in Tag.all()]
        }


@register.inclusion_tag(join(dirname(__file__), 'recipe_titlecard.html'))
def recipe_titlecard(recipe):
    return { 'recipe' : recipe, 'stickies' : [s for s in recipe.stickies] }


@register.inclusion_tag(join(dirname(__file__), 'recipe_fullview.html'))
def recipe_fullview(recipe):
    return { 'recipe' : recipe,
             'stickies' : [s for s in recipe.stickies],
             }


@register.inclusion_tag(join(dirname(__file__), 'recipe_fullview.js'))
def recipe_fullview_viewmodel(json):
    return { 'json' : json }
