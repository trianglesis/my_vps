from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tinymce.models import HTMLField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'tria_tags'
        verbose_name = '[Blog] Tag'
        verbose_name_plural = '[Blog] Tags'

    def __str__(self):
        return f'{self.id}-{self.name}'


class Post(models.Model):
    """
    Use 'django-tinymce'
    https://django-tinymce.readthedocs.io/en/latest/installation.html
    TODO: Use 'django-filebrowser'
    https://github.com/sehmaschine/django-filebrowser
    """
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    body = HTMLField()

    meta_description = models.CharField(max_length=255, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag,
                                  blank=True,
                                  related_name='post_rel_tag'
                                  )

    class Meta:
        ordering = ["-publish_date"]
        managed = True
        db_table = 'tria_posts'
        # unique_together = (
        #     (
        #         'title',
        #         'subtitle',
        #         'slug',
        #     ),
        # )
        verbose_name = '[Blog] Post'
        verbose_name_plural = '[Blog] Posts'

    def __str__(self):
        return f'{self.id} - {self.title}-{self.author}'

    def get_absolute_url(self):
        """
        Generate URL for each published post.
        Example:
        <loc>http://Site.objects.get_current().domain/post/raspberry-5-test-to-speech-using-piper</loc>
        https://docs.djangoproject.com/en/5.0/ref/contrib/sites/#module-django.contrib.sites
        Do not add here domain
        :return:
        """
        return f"/post/{self.slug}"