import logging

from django.core.management import BaseCommand
from django.contrib.sites.models import Site

from django.contrib.redirects.models import Redirect


from blog.models import Post
from main.models import (NetworkVisitorsAddresses, URLPathsVisitors, UserAgentVisitors, RequestGetVisitors, RequestPostVisitors)

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
            if mode == 'visitors_select':
                visitors = NetworkVisitorsAddresses.objects.all()
                print(f"Overall visits: {visitors.count()}")

                if method == 'select_and_show':
                    visitor = visitors.first().values()
                    print(f"visitor: {visitor}")

                elif method == 'select_and_sort_insert':
                    """
                    Now select all visitors and save future foreign keys to other tables
                    """
                    for i, visitor in enumerate(visitors, 1):
                        rel_url_path, created = URLPathsVisitors.objects.update_or_create(url_path=visitor.url_path)
                        rel_user_agent, created = UserAgentVisitors.objects.update_or_create(user_agent=visitor.user_agent)
                        rel_request_get, created = RequestGetVisitors.objects.update_or_create(request_get_args=visitor.request_get_args)
                        rel_request_post, created = RequestPostVisitors.objects.update_or_create(request_post_args=visitor.request_post_args)
                        visitor.rel_url_path = rel_url_path
                        visitor.rel_user_agent = rel_user_agent
                        visitor.rel_request_get = rel_request_get
                        visitor.rel_request_post = rel_request_post
                        visitor.save()
                        print(f"Processed {i} of {visitors.count()} visitors")

                elif method == 'delete_unwanted_field_data':
                    """
                    Now we can delete data from fields we no longer use, or make a migration to delete
                    """
                    for i, visitor in enumerate(visitors, 1):
                        print(f"Processed {i} of {visitors.count()} visitors")

                elif method == 'select_urls_and_update_redirects':
                    """
                    Method checks all actual blog posts migrated from old blog
                    and see if its SLUG appeared with an old an wrong path of visitors URL.
                    When true - creates a correction redirect from wrong URL to correct URL.
                    """
                    site = Site.objects.first()
                    all_urls = URLPathsVisitors.objects.all().order_by('url_path')
                    all_blog_posts = Post.objects.all().order_by('slug')
                    for blog_post in all_blog_posts:
                        # Better use exact match, since some slugs are different but have shorter sentence with similar words
                        possible_bad_url_path = all_urls.filter(url_path__exact=f"/{blog_post.slug}")
                        # Only assign if there is one result
                        if possible_bad_url_path.count() == 1:
                            print(f"Old URL found in visitors table with the slug of real blog post:"
                                  f"\nPost: {blog_post.slug}"
                                  f"\nURL: {possible_bad_url_path.values()}")
                            # Now create a new redirect:
                            redirect, created = Redirect.objects.update_or_create(
                                site=site,
                                old_path=possible_bad_url_path.first().url_path,
                                defaults={"new_path": f"/blog/post/{blog_post.slug}/"}
                            )
                            if created:
                                print(f"New redirect created:"
                                      f"\n\told_path: {redirect.old_path}"
                                      f"\n\tnew_path: {redirect.new_path}"
                                      f"")
                        # Notify if the same url is appeared more than once:
                        elif possible_bad_url_path.count() > 1:
                            print("Bad URL appeared more than one time in visitors table URLs:"
                                  f"\nPost: {blog_post.slug}"
                                  f"\nURL: {possible_bad_url_path.values()}")
                        # End
                        else:
                            pass







"""
python manage.py visitors_sorting --mode=visitors_select --method=select_and_show
python manage.py visitors_sorting --mode=visitors_select --method=select_and_sort_insert
python manage.py visitors_sorting --mode=visitors_select --method=select_urls_and_update_redirects



visitors_url_path visitors_user_agent visitors_request_get visitors_request_post visitors_agents
"""