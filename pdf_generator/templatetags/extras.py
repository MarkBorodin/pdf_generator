from django import template

register = template.Library()


def myround(x, prec=2, base=.05):
    return round(base * round(float(x + 0.01)/base), prec)


register.filter('myround', myround)


def prices_format(x):
    negative = False
    if '-' in x:
        negative = True
        x = x.replace('-', '')
    x_str, float_part = x.split(sep='.')[0], x.split(sep='.')[1]
    if len(x_str) > 3:
        x_str = x_str[:-3] + '’' + x_str[-3:]
        return f'{x_str}.{float_part}' if x is not negative else f'-{x_str}.{float_part}'
    else:
        return x if not negative else f'-{x}'


register.filter('prices_format', prices_format)


@register.simple_tag
def define(obj):
    return obj
