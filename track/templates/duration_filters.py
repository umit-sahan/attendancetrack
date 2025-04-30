from django import template

register = template.Library()

@register.filter
def duration_to_hours(value):
    if value:
        return round(value.total_seconds() / 3600, 2)
    return 0
