from django import template

register = template.Library()


def multiply(value, arg):
    return value * arg


register.filter('multiply', multiply)