# classifier/templatetags/nav_tags.py
from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def active_link(request, url_name):
    """
    Retourne 'active' si l'URL actuelle correspond au nom d'URL donné
    """
    try:
        if request.resolver_match.url_name == url_name:
            return "active"
    except:
        pass
    return ""