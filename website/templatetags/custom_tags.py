from django import template

register = template.Library()

def split(str, key):
    
    return str.split(key)

register.filter('split', split)