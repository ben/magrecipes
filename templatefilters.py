from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.filter
def localcapfirst(value):
    return "(%s)" % value #str(value).capitalize()
