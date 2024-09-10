from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Divide el valor de la cadena por el argumento especificado"""
    return value.split(arg)
