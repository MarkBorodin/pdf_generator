from django import template

register = template.Library()


def myround(x, prec=2, base=.05):
    return round(base * round(float(x + 0.01)/base), prec)


register.filter('myround', myround)
