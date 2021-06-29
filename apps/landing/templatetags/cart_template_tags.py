from django import template

register = template.Library()

@register.filter
def post_categories(value):
    return 0

