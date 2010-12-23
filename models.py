from google.appengine.ext import db

class Recipe(db.Model):
    title = db.StringProperty()
    instructions = db.TextProperty()
    categories = db.ListProperty(db.Category)

class Ingredient(db.Model):
    name = db.StringProperty()

class QuantifiedIngredient(db.Model):
    ingredient = db.ReferenceProperty(Ingredient)
    quantity = db.StringProperty()
    note = db.StringProperty()
    recipe = db.ReferenceProperty(Recipe, collection_name='ingredients')

