import logging

from django import template

register = template.Library()
log = logging.getLogger("core")


@register.simple_tag(takes_context=True)
def tab_active(context, arg):
    if context['objects']:
        obj = context['objects']
        role = obj.get('role', None)
        if not role == arg:
            return False
        return True
