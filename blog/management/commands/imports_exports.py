import logging
import datetime
import re

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import BaseCommand
from blog.models import WptriaPosts, Post, Tag

log = logging.getLogger("core")


class Command(BaseCommand):
    help = 'Local execution of internal methods.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--mode', type=str, help='Select mode to use')
        parser.add_argument('--method', type=str, help='method')
        parser.add_argument('--value', type=str, help='value')
        parser.add_argument('--key', type=str, help='key')

    def handle(self, *args, **kwargs):
        mode = kwargs.get('mode', None)
        method = kwargs.get('method', None)
        value = kwargs.get('value', '')
        key = kwargs.get('key', '')

        if mode:
            if mode == 'WP_old_database_filter':
                print(f"Run mode: WP_old_database_filter, method: {method}")
                if method == 'select_and_show':
                    posts = WptriaPosts.objects.all()
                    for post in posts:
                        print(f"posts: {post.post_title}")
                elif method == 'select_and_import':
                    posts = WptriaPosts.objects.all()
                    for post in posts:
                        if post.post_name:
                            print(f"Importing: {post.post_name}, date: {post.post_date}")
                            imported = Post(
                                title=post.post_title,
                                slug=post.post_name,
                                body=post.post_content,
                                publish_date=post.post_date,
                                date_created=post.post_date,
                                author=User.objects.all().first(),
                                site=Site.objects.all().first(),
                                published=False,
                            )
                            # if not imported.slug == post.post_name:
                            imported.save()
                elif method == 'select_and_tag':
                    keywords = ['Python', 'python']
                    for post in Post.objects.all():
                        if any([word in post.body for word in keywords]):
                            tag = Tag.objects.get(name='python')
                            print(f"This post is related to tag 'python': {post.title}")
                            post.tags.add(tag)
                            post.save()
                elif method == 'select_imported_body_with_pic':
                    """
                    OLD:
                    - http://www.trianglesis.org.ua/wp-content/uploads/2019/10/image.png
                    New:
                    
                    """
                    old_wp = re.compile(r"http://www\.trianglesis\.org\.ua/wp-content/uploads/")
                    new_blog_url = "https://trianglesis.org.ua/static/old-wordpress/"
                    for post in Post.objects.all():
                        if '/wp-content/uploads/' in post.body:
                            post.body = old_wp.sub(new_blog_url, post.body)
                            post.save()
                            print(f"Post with old pics: {post.title} - {post.id} - replace URL")
                            break




"""
python manage.py imports_exports --mode=WP_old_database_filter --method=select_and_show
python manage.py imports_exports --mode=WP_old_database_filter --method=select_and_import
python manage.py imports_exports --mode=WP_old_database_filter --method=select_and_tag
python manage.py imports_exports --mode=WP_old_database_filter --method=select_imported_body_with_pic
"""