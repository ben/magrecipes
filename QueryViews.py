import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template.context import RequestContext
from django.utils import simplejson

from models import Recipe, Ingredient, Tag
from helpers import uniq


def bucketize(arr, extractor):
    buckets = {}
    for i in arr:
        key = extractor(i).lower()[:1]
        if not key in buckets:
            buckets[key] = []
        buckets[key].append(i)
    keys = buckets.keys()
    keys.sort()
    return buckets,keys


################################################################################
class RecipesByTitleHandler(webapp.RequestHandler):
    def get(self):
        q = Recipe.all()
        recipes = [r for r in q]
        buckets,keys = bucketize(recipes, lambda x: x.title)
        templatevalues = RequestContext(self.request, {
            'recipes' : recipes,
            'buckets' : buckets,
            'keys' : keys,
            })

        path = os.path.join(os.path.dirname(__file__), 'recipes_by_title.html')
        self.response.out.write(template.render(path, templatevalues))
        

################################################################################
class IngredientsByNameHandler(webapp.RequestHandler):
    def get(self):
        q = Ingredient.all()
        ingredients = [i for i in q if i.quantifiedingredient_set.count() > 0]
        buckets,keys = bucketize(ingredients, lambda x: x.name)
        templatevalues = RequestContext(self.request, {
                'ingredients' : ingredients,
                'buckets' : buckets,
                'keys' : keys
                })
        path = os.path.join(os.path.dirname(__file__), 'ingredients_by_name.html')
        self.response.out.write(template.render(path, templatevalues))


################################################################################
class RecipesByIngredientHandler(webapp.RequestHandler):
    def get(self, ingredient_key):
        i = Ingredient.get(ingredient_key)
        if i == None:
            # TODO: error page?
            return

        # Gather all the recipes for all the QIs for this ingredient
        recipes = uniq([qi.recipe for qi in i.quantifiedingredient_set],
                       lambda x: x.title)

        buckets,keys = bucketize(recipes, lambda x: x.title)
        templatevalues = RequestContext(self.request, {
                'ingredient' : i,
                'recipes' : recipes,
                'buckets' : buckets,
                'keys' : keys
                })
        path = os.path.join(os.path.dirname(__file__), 'recipes_by_ingredient.html')
        self.response.out.write(template.render(path, templatevalues))
        

################################################################################
class RecipesByStickyHandler(webapp.RequestHandler):
    def get(self):
        have = []
        havenot = []
        for r in Recipe.all():
            if r.stickies.count(1) > 0: have.append(r)
            else: havenot.append(r)
        templatevalues = RequestContext(self.request, {
                'have' : have,
                'havenot' : havenot,
                })
        path = os.path.join(os.path.dirname(__file__), 'recipes_by_sticky.html')
        self.response.out.write(template.render(path, templatevalues))


################################################################################
class TagsByNameHandler(webapp.RequestHandler):
    def get(self):
        q = Tag.all()
        tags = [t for t in q]
        buckets,keys = bucketize(tags, lambda t: t.tag)
        templatevalues = RequestContext(self.request, {
                'tags' : tags,
                'buckets' : buckets,
                'keys' : keys,
                })
        path = os.path.join(os.path.dirname(__file__), 'tags_by_name.html')
        self.response.out.write(template.render(path, templatevalues))


################################################################################
class RecipesByTagHandler(webapp.RequestHandler):
    def get(self, tag_name):
        t = Tag.get_by_name(tag_name)
        if t == None:
            # TODO: error page?
            return

        # Gather all the recipes for all the QIs for this ingredient
        recipes = uniq([Recipe.get(key) for key in t.tagged],
                       lambda x: x.title)

        buckets,keys = bucketize(recipes, lambda x: x.title)
        templatevalues = RequestContext(self.request, {
                'tag' : t,
                'recipes' : recipes,
                'buckets' : buckets,
                'keys' : keys
                })
        path = os.path.join(os.path.dirname(__file__), 'recipes_by_tag.html')
        self.response.out.write(template.render(path, templatevalues))
        

        

