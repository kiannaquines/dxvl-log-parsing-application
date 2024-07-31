from django import template

register = template.Library()

@register.simple_tag
def concat_str(string1, string2):
    return f"{string1}{string2}"