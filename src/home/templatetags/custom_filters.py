from django import template
from wagtail.rich_text import RichText
import re

register = template.Library()

@register.filter
def split(value, arg):
    """Divide el valor de la cadena por el argumento especificado"""
    return value.split(arg)

@register.filter
def remove_empty_tags(value):
    """
    Elimina etiquetas vacías o con solo espacios en el contenido HTML.
    """
    if value:
        # Remover etiquetas vacías o con solo espacios
        cleaned_value = re.sub(r'<(p|div|h[1-6]|span)[^>]*>\s*(<br/>)?\s*</\1>', '', str(value), flags=re.MULTILINE)
        return cleaned_value.strip()  # Remover espacios adicionales al final o principio
    return value