from google.appengine.ext import db
import logging
from helpers import to_dict

class Recipe(db.Model):
    title = db.StringProperty()
    instructions = db.TextProperty()
    yeeld = db.StringProperty()
    source = db.StringProperty()

    ingredient_list = db.ListProperty(db.Key)

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

    def to_dict(self):
        if self.is_saved(): return {
            'key' : str(self.key()),
            'january' : self.january,
            'february' : self.february,
            'march' : self.march,
            'april' : self.april,
            'may' : self.may,
            'june' : self.june,
            'july' : self.july,
            'august' : self.august,
            'september' : self.september,
            'october' : self.october,
            'november' : self.november,
            'december' : self.december,
            'title' : self.title,
            'instructions' : self.instructions,
            'ingredients' : [qi.to_dict() for qi in db.get(self.ingredient_list)],
            'images' : [i.to_dict() for i in self.images],
            'stickies' : [s.to_dict() for s in self.stickies],
            'yeeld' : self.yeeld,
            'source' : self.source,
            }

        # Unsaved recipe; default values
        return  {
            'key' : '',
            'january' : False,
            'february' : False,
            'march' : False,
            'april' : False,
            'may' : False,
            'june' : False,
            'july' : False,
            'august' : False,
            'september' : False,
            'october' : False,
            'november' : False,
            'december' : False,
            'title' : '',
            'instructions' : '',
            'ingredients' : [],
            'images' : [i.to_dict() for i in Image.all().run()
                        if i.recipe == None],
            'stickies' : [],
            'yeeld' : '',
            'source' : '',
            }

    def set_from_dict(self, d):
        logging.debug(d)
        self.title        = d['title']
        self.instructions = d['instructions']
        self.yeeld        = d['yeeld']
        self.source       = d['source']
        self.january      = bool(d['january'])
        self.february     = bool(d['february'])
        self.march        = bool(d['march'])
        self.april        = bool(d['april'])
        self.may          = bool(d['may'])
        self.june         = bool(d['june'])
        self.july         = bool(d['july'])
        self.august       = bool(d['august'])
        self.september    = bool(d['september'])
        self.october      = bool(d['october'])
        self.november     = bool(d['november'])
        self.december     = bool(d['december'])
        self.put()

        # Update images to point here
        for i in d['images']:
            img = Image.get(i['key'])
            img.recipe = self
            img.put()

        # Replace ingredients with new ones
        db.delete(self.ingredient_list)
        self.ingredient_list = []
        for ivm in d['ingredients']:
            ing = Ingredient.get_or_insert(ivm['name'],
                                           name=ivm['name'])
            qi = QuantifiedIngredient(ingredient=ing,
                                      quantity=ivm['quantity'],
                                      note=ivm['note'],
                                      recipe=self)
            qi.put()
            self.ingredient_list.append(qi.key())
        self.put()

    def delete(self):
        db.delete(self.ingredient_list)
        db.delete(self.key())
            

class Ingredient(db.Model):
    name = db.StringProperty()

class QuantifiedIngredient(db.Model):
    ingredient = db.ReferenceProperty(Ingredient)
    quantity = db.StringProperty()
    note = db.StringProperty()
    recipe = db.ReferenceProperty(Recipe)

    def to_dict(self):
        return {
            'name' : self.ingredient.name,
            'quantity' : self.quantity,
            'note' : self.note,
            }

class Image(db.Model):
    data   = db.BlobProperty()
    recipe = db.ReferenceProperty(Recipe, collection_name="images")

    def to_dict(self):
        return {'key' : str(self.key())}

class ResizedImage(db.Model):
    size = db.IntegerProperty()
    image = db.ReferenceProperty(Image, collection_name="sized_images")
    data = db.BlobProperty()

class Sticky(db.Model):
    recipe = db.ReferenceProperty(Recipe, collection_name="stickies")
    text = db.TextProperty()

    def to_dict(self):
        return {
            'text' : self.text,
            'key' : str(self.key()),
            }
