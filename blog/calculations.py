from __future__ import absolute_import, unicode_literals
import logging

from django.db.models import Q
from blog.models import Post, Hits
from main.models import URLPathsVisitors

log = logging.getLogger("core")

def calculate_hits():
    """
    Select all blog posts and get all hits from visitor URL table where post-slug is found.
    :return:
    """
    log.info(f"Start task calculating visitors hits at blog posts.")
    all_urls = URLPathsVisitors.objects.all().order_by('url_path')
    all_blog_posts = Post.objects.all().order_by('slug')
    for blog_post in all_blog_posts:
        visited_urls = all_urls.filter(
            Q(url_path__exact=f"/{blog_post.slug}") |
            Q(url_path__exact=f"/post/{blog_post.slug}") |
            Q(url_path__exact=f"/blog/post/{blog_post.slug}/")
        )
        # There can be multiple items:
        if visited_urls.count() > 1:
            sum_hits = 0
            for visit in visited_urls:
                sum_hits += visit.visitor_rel_url_path.all().count()
            hits, _ = Hits.objects.update_or_create(
                post=blog_post,
                defaults={"hits": sum_hits},
            )
        # One visit - save the counter
        elif visited_urls.count() == 1:
            visit = visited_urls.first()
            hits, _ = Hits.objects.update_or_create(
                post=blog_post,
                defaults={"hits": visit.visitor_rel_url_path.all().count()},
            )
    return True