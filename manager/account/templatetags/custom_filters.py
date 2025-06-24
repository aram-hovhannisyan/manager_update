# from django import template
# from django.utils.dateformat import DateFormat

# register = template.Library()

# @register.filter
# def format_datetime(value):
#     if not value:
#         return
#     df = DateFormat(value)
#     formatted_date = df.format('d.m.Y H:i')
#     return formatted_date

# @register.filter
# def format_date(value):
#     if not value:
#         return value
#     return value.strftime('%d.%m.%Y')

# @register.filter
# def sub(value, arg):
#     return value - arg

# @register.filter
# def add(value, arg):
#     return value + arg

from django import template
from django.utils.dateformat import DateFormat

register = template.Library()

@register.filter
def format_datetime(value):
    if not value:
        return
    df = DateFormat(value)
    formatted_date = df.format('d.m.Y H:i')
    return formatted_date

@register.filter
def format_date(value):
    if not value:
        return value
    return value.strftime('%d.%m.%Y')

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def add(value, arg):
    return value + arg

@register.filter
def abs_sub(value, arg):
    if value > arg:
        return value - arg
    return arg - value