from google.appengine.ext import db

class Recipe(db.Model):
    title = db.StringProperty()
    instructions = db.TextProperty()

    january   = db.BooleanProperty()
    february  = db.BooleanProperty()
    march     = db.BooleanProperty()
    april     = db.BooleanProperty()
    may       = db.BooleanProperty()
    june      = db.BooleanProperty()
    july      = db.BooleanProperty()
    august    = db.BooleanProperty()
    september = db.BooleanProperty()
    october   = db.BooleanProperty()
    november  = db.BooleanProperty()
    december  = db.BooleanProperty()

class Ingredient(db.Model):
    name = db.StringProperty()

class QuantifiedIngredient(db.Model):
    ingredient = db.ReferenceProperty(Ingredient)
    quantity = db.StringProperty()
    note = db.StringProperty()
    recipe = db.ReferenceProperty(Recipe, collection_name='ingredients')

