from django import template
from django.utils.html import format_html
from markdownx.utils import markdownify
from bs4 import BeautifulSoup
register = template.Library()


@register.simple_tag
def count_badge(count=0, false_colour='info', true_colour='danger'):
    badge_colour = false_colour
    if count > 0:
        badge_colour = true_colour

    return format_html(
        '&nbsp;<sup><span class="badge badge-pill badge-{}">{}</span></sup>',
        badge_colour,
        count)


@register.filter
def textify(data):
    """Returns plain text by converting MD to HTML then strips HTML markup and
    excess spaces / new line characters"""
    html_data = markdownify(data)
    text_data = ''.join(BeautifulSoup(
        html_data, "html.parser").findAll(text=True))

    return ' '.join(text_data.replace('\n', ' ').replace('\r', '').split())
