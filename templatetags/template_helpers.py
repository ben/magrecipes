from google.appengine.ext import webapp
from django.template import Node, NodeList, Library
from google.appengine.api import users

register = webapp.template.create_template_register()


################################################################################
@register.tag(name="if_admin")
def do_if_admin(parser, token):
    nodelist_true = parser.parse(('else', 'endif',))
    nodelist_false = NodeList()
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif',))
        parser.delete_first_token()
    return IfAdminNode(nodelist_true, nodelist_false)

class IfAdminNode(Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        if (users.is_current_user_admin()):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
