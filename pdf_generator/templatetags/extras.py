from django import template

register = template.Library()


def myround(x, prec=2, base=.05):
    return round(base * round(float(x + 0.01)/base), prec)


register.filter('myround', myround)


def prices_format(x):
    x_str = x.split(sep='.')[0]
    if len(x_str) > 3:
        x_str = x_str[:-3] + '’' + x_str[-3:]
        return x_str
    else:
        return x


register.filter('prices_format', prices_format)


@register.simple_tag
def define(obj):
    return obj
