# apps/templatetags/custom_tags.py
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='currency')
@stringfilter
def currency(value):
    try:
        value = float(value)
        formatted_value = '{:,.2f}'.format(value).replace('.', 'X').replace(',', '.').replace('X', ',')
        return f'R$ {formatted_value}'
    except ValueError:
        return value
