import logging

from django.core.management import BaseCommand
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






"""
python manage.py visitors_sorting --mode=visitors_select --method=select_and_show

python manage.py visitors_sorting --mode=visitors_select --method=select_and_sort_insert

"""