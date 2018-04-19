from django import template

register = template.Library()

#@register.simple_tag
def get_field(obj, field):
    return obj.get_field(field)

register.filter('get_field', get_field)
