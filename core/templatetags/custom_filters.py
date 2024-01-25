from django import template
from datetime import datetime
from django.utils.dateformat import format

register = template.Library()

@register.filter
def format_date(value):
    if not isinstance(value, datetime):
        return value
    
    day = value.strftime("%d")
    if day.endswith('1'):
        day += 'st'
    elif day.endswith('2'):
        day += 'nd'
    elif day.endswith('3'):
        day += 'rd'
    else:
        day += 'th'
    
    formatted_date = value.strftime(f"{day} %B %Y")
    return formatted_date


@register.filter(name='format_datetime')
def format_datetime(value):
    if isinstance(value, datetime):
        formatted_date = format(value, 'jS F Y h:i:s A')
        return formatted_date
    return value

@register.filter
def concat_string(value_1, value_2):
    return str(value_1) + "-" + str(value_2)

@register.filter
def concatenate_ids(plan_id, id):
    truncated_plan_id = plan_id[:6]
    concatenated_id = f"{truncated_plan_id}-{id}"
    return concatenated_id