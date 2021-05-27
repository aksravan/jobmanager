from django import template

register = template.Library()

@register.filter
def get_value(dictionary, key):
    try:
        return dictionary[key]
    except:
        return []

@register.filter
def get_location(resume):
    return '/'.join(str(resume).split('/')[1:])

