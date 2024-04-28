import logging
from hashlib import blake2b

from django.core.management import BaseCommand
from django.contrib.sites.models import Site

from django.contrib.redirects.models import Redirect
from django.db.models import Q

from blog.models import Post, Hits
from main.models import (NetworkVisitorsAddresses, URLPathsVisitors, UserAgentVisitors, RequestGetVisitors, RequestPostVisitors)

log = logging.getLogger("core")

def hashify(item_col):
    h = blake2b(digest_size=8)
    h.update(item_col.encode('utf-8'))
    return h.hexdigest()


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
            elif method == 'calculate_hits':
                """
                Check blog post slugs in visitors table and calculate visitors counter.
                This is pre-test, later taskify it.
                """
                all_urls = URLPathsVisitors.objects.all().order_by('url_path')
                all_blog_posts = Post.objects.all().order_by('slug')
                for blog_post in all_blog_posts:
                    # Use OR
                    visited_urls = all_urls.filter(
                        # Old format: get hits from it too
                        Q(url_path__exact=f"/{blog_post.slug}") |
                        # Wrong format of bad sitemap xml: get hits from it too
                        Q(url_path__exact=f"/post/{blog_post.slug}") |
                        # New format and with redirect
                        Q(url_path__exact=f"/blog/post/{blog_post.slug}/")
                    )
                    # There can be multiple items:
                    if visited_urls.count() > 1:
                        # Sum all counters to one
                        sum_hits = 0
                        for visit in visited_urls:
                            sum_hits += visit.visitor_rel_url_path.all().count()

                        print(f"Blog post visited some amount of times: "
                              f"\n\tPost: {blog_post.slug}"
                              f"\n\tHits (sum): {sum_hits}")
                        hits, created = Hits.objects.update_or_create(
                            post=blog_post,
                            defaults={"hits": sum_hits},
                        )
                        if created:
                            print(f"New post hits counter created!")

                    # One visit - save the counter
                    elif visited_urls.count() == 1:
                        visit = visited_urls.first()
                        print(f"Blog post visited some amount of times: "
                              f"\n\tPost: {blog_post.slug}"
                              f"\n\tHits: {visit.visitor_rel_url_path.all().count()}")
                        hits, created = Hits.objects.update_or_create(
                            post=blog_post,
                            defaults={"hits": visit.visitor_rel_url_path.all().count()},
                        )
                        if created:
                            print(f"New post hits counter created!")
                    # Visible close
                    else:
                        pass
        elif mode == 'internal':
            if method == 'hashify':
                items = URLPathsVisitors.objects.all()
                for item in items:
                    # Save method is now overridden, just re-save for hashing
                    # item.hash = hashify(item_col=item.url_path)
                    item.save()
                items = UserAgentVisitors.objects.all()
                for item in items:
                    # Save method is now overridden, just re-save for hashing
                    # item.hash = hashify(item_col=item.user_agent)
                    item.save()
                items = RequestGetVisitors.objects.all()
                for item in items:
                    # Save method is now overridden, just re-save for hashing
                    # item.hash = hashify(item_col=item.request_get_args)
                    item.save()
                items = RequestPostVisitors.objects.all()
                for item in items:
                    # Save method is now overridden, just re-save for hashing
                    # item.hash = hashify(item_col=item.request_post_args)
                    item.save()



"""
python manage.py visitors_sorting --mode=visitors_select --method=select_and_show
python manage.py visitors_sorting --mode=visitors_select --method=select_and_sort_insert
python manage.py visitors_sorting --mode=visitors_select --method=select_urls_and_update_redirects
python manage.py visitors_sorting --mode=visitors_select --method=calculate_hits

python manage.py visitors_sorting --mode=internal --method=hashify


visitors_url_path visitors_user_agent visitors_request_get visitors_request_post visitors_agents
visitors_url_path visitors_user_agent visitors_request_get visitors_request_post visitors_agents
"""