import logging

from django import template

from blog.models import Tag, Post

register = template.Library()
log = logging.getLogger("core")


@register.simple_tag(takes_context=True)
def selector_validate(context, exclude_key=None, update_context=False):
    """
    Looks in context for selector dict.
    Remove duplicates or empty values.
    Attach selector to paginator and other sorting or filtering buttons.
    See pagination.html
    """
    selector = context.get('selector')
    sel_str = ''
    for sel_k, sel_v in selector.items():
        if not sel_k == exclude_key:
            if sel_v:
                sel = f'{sel_k}={sel_v}&'
                sel_str += sel
    if sel_str.endswith('&'):
        sel_str = sel_str.rstrip(sel_str[-1])
    if update_context:
        context[update_context] = sel_str
        return ''
    else:
        return sel_str


@register.simple_tag()
def list_tags():
    return Tag.objects.all()


@register.simple_tag()
def list_last_posts_and_tags(limit_posts=3, limit_tags=5):
    main_data = dict(
        posts=Post.objects.filter(published=True).order_by("-publish_date")[limit_posts],
        tags=Tag.objects.all()[limit_tags],
    )
    return main_data


@register.simple_tag()
def posts_last(limit=3):
    return Post.objects.filter(published=True).order_by("-publish_date")[:limit]


@register.simple_tag()
def posts_random(limit=5):
    return Post.objects.filter(published=True).order_by("?")[:limit]