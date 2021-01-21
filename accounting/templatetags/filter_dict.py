from django import template


register = template.Library()


@register.filter('get_dict_value')
def get_dict_value(d, key):
    return d[key]
