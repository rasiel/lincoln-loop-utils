from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

class ComparisonNode(template.Node):
    def __init__(self, var, nodelist_true, nodelist_false):
        self.var = var
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        value = template.resolve_variable(self.var, context)
        file_bits = value.split('.')
        if file_bits[-1] in ('jpg', 'jpeg', 'png', 'gif', 'bmp'):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

@register.tag
def if_is_image(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'%s' tag takes one arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return ComparisonNode(bits[1], nodelist_true, nodelist_false)
    
@register.simple_tag
def media_url():
    return settings.MEDIA_URL