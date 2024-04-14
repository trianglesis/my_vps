import logging

from django import template

from blog.models import Tag

register = template.Library()
log = logging.getLogger("core")


@register.simple_tag()
def list_tags():
    return Tag.objects.all()