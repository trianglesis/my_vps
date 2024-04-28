from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from tinymce.models import HTMLField

from core.setup_logic import Credentials


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
    title = models.CharField(max_length=255)
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
                                  related_name='post_rel_tag',
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
        return f"/blog/post/{self.slug}/"

    def get_absolute_hostname_url(self):
        return f"{Credentials.SITE_HTTP}/blog/post/{self.slug}/"

class Hits(models.Model):
    hits = models.IntegerField(default=0)
    post = models.OneToOneField(Post,
                                related_name='hits_rel_post',
                                # If post delete do not keep hits
                                on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tria_posts_hits'
        verbose_name = '[Blog] Hit'
        verbose_name_plural = '[Blog] Hits'


class WptriaPosts(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    post_author = models.PositiveBigIntegerField()
    post_date = models.DateTimeField(blank=True, null=True)
    post_date_gmt = models.DateTimeField(blank=True, null=True)
    post_content = models.TextField(db_collation='utf8mb3_general_ci')
    post_title = models.TextField(db_collation='utf8mb3_general_ci')
    post_excerpt = models.TextField(db_collation='utf8mb3_general_ci')
    post_status = models.CharField(max_length=20, db_collation='utf8mb3_general_ci')
    comment_status = models.CharField(max_length=20, db_collation='utf8mb3_general_ci')
    post_name = models.CharField(max_length=200, db_collation='utf8mb3_general_ci')
    post_modified = models.DateTimeField(blank=True, null=True)
    post_modified_gmt = models.DateTimeField(blank=True, null=True)
    post_content_filtered = models.TextField(db_collation='utf8mb3_general_ci')
    guid = models.CharField(max_length=255, db_collation='utf8mb3_general_ci')

    class Meta:
        managed = False
        db_table = 'wptria_posts'
