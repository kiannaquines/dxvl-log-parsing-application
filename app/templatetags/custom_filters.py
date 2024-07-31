from django import template

register = template.Library()

@register.filter
def custom_range(value):
    return range(int(value))


@register.filter
def custom_range_plus_one(value):
    return range(int(value) + 1)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)