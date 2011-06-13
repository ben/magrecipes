from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def join(collection, method, joinstr):
    strs = []
    for c in collection:
        strs.append(getattr(c, method)())
    return joinstr.join(strs)

def foobar(value):
    return "(%s)" % str(value)

register.filter(foobar)
