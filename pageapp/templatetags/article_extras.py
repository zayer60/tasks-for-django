from django import template
from django.template.defaultfilters import stringfilter
import datetime

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')


@register.filter
@stringfilter
def lower(value):
    return value.lower()


@register.filter(expects_localtime=True)
def businesshours(value):
    try:
        return 9 <= value.hour < 17
    except AttributeError:
        return ''


@register.simple_tag
def current_time(time_format):
    return datetime.datetime.now().strftime(time_format)

# @register.simple_tag(takes_context=True)
#def current_time(context, time_format):
#    timezone = context['timezone']
#    return your_get_current_time_method(timezone, time_format)



# register.filter('cut', cut)
# register.filter('lower', lower)
