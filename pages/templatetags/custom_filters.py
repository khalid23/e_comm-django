from django import template

register = template.Library()

@register.filter(name='split_sizes')
def split_sizes(value):
    if value is not None:
        return value.split(', ')
    return value
