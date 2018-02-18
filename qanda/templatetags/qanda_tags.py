from django import template
from django.utils.html import format_html
register = template.Library()

@register.simple_tag
def count_badge(count=0, false_colour='info', true_colour='danger' ):
    badge_colour = false_colour
    if count > 0:
        badge_colour = true_colour

    return format_html(
        '&nbsp;<sup><span class="badge badge-pill badge-{}">{}</span></sup>',
        badge_colour,
        count)
