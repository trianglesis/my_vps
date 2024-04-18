import logging

from django import template

from blog.models import Tag, Post

register = template.Library()
log = logging.getLogger("core")


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
def last_posts(limit=3):
    return Post.objects.filter(published=True).order_by("-publish_date")[:limit]