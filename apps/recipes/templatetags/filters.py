from django import template

register = template.Library()

@register.filter

def fraction_to_unicode(value):
    fractions = {
        '1/2': '½',
        '1/4': '¼',
        '3/4': '¾',
        '1/3': '⅓',
        '2/3': '⅔',
        '1/5': '⅕',
        '2/5': '⅖',
        '3/5': '⅗',
        '4/5': '⅘',
        '1/6': '⅙',
        '5/6': '⅚',
        '1/8': '⅛',
        '3/8': '⅜',
        '5/8': '⅝',
        '7/8': '⅞',
    }

    for frac, unicode_char in fractions.items():
        value = value.replace(frac, unicode_char)
    return value