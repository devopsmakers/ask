from django import template
from django.utils.html import format_html
register = template.Library()

from ..models import Question

@register.simple_tag
def unanswered_badge():
    unanswered = Question.objects.unanswered().count()
    badge_colour = 'info'
    if unanswered > 0:
        badge_colour = 'danger'

    return format_html(
        '&nbsp;<sup><span class="badge badge-pill badge-{}">{}</span></sup>',
        badge_colour,
        unanswered)

@register.simple_tag
def answered_badge():
    answered = Question.objects.answered().count()
    badge_colour = 'success'

    return format_html(
        '&nbsp;<sup><span class="badge badge-pill badge-{}">{}</span></sup>',
        badge_colour,
        answered)
