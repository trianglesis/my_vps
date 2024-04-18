from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.contrib.sites.models import Site

class BlogSitemap(Sitemap):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/sitemaps/
    """
    changefreq = "daily"
    priority = 0.5

    def items(self):
        obj = Post.objects.filter(published=True)
        return obj

    def lastmod(self, obj):
        return obj.publish_date