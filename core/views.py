import datetime
import logging

from hashlib import blake2b

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings
from django.urls import path
from django.utils import timezone

from ipware import get_client_ip

from main.models import NetworkVisitorsAddresses

log = logging.getLogger("dev")

"""
Conf https://github.com/un33k/django-ipware
"""


def response_error_handler(request, exception=None):
    # log.debug(f"request: \n{request.headers}, \n{request.user} \n{request.path}, \n{request.get_full_path}, \n{request.path_info}")
    u_agent = request.META['HTTP_USER_AGENT']
    client_ip, is_routable = get_client_ip(request)
    save_visit(client_ip, is_routable, u_agent, request.path)
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def page_not_found_view(request, exception=None):
    # log.debug(f"request: \n{request.headers}, \n{request.user} \n{request.path}, \n{request.get_full_path}, \n{request.path_info}")
    u_agent = request.META['HTTP_USER_AGENT']
    client_ip, is_routable = get_client_ip(request)
    save_visit(client_ip, is_routable, u_agent, request.path)
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def bad_request_view(request, exception=None):
    # log.debug(f"request: \n{request.headers}, \n{request.user} \n{request.path}, \n{request.get_full_path}, \n{request.path_info}")
    u_agent = request.META['HTTP_USER_AGENT']
    client_ip, is_routable = get_client_ip(request)
    save_visit(client_ip, is_routable, u_agent, request.path)
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def permission_denied_view(request, exception=None):
    # log.debug(f"request: \n{request.headers}, \n{request.user} \n{request.path}, \n{request.get_full_path}, \n{request.path_info}")
    u_agent = request.META['HTTP_USER_AGENT']
    client_ip, is_routable = get_client_ip(request)
    save_visit(client_ip, is_routable, u_agent, request.path)
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def save_visit(ip, is_routable, user_agent, url_path):
    # Making unique hash for ip + user agent + path requested
    hashed_agent_path = f"{ip}-{user_agent}-{url_path}"
    h = blake2b(digest_size=64)
    h.update(hashed_agent_path.encode('utf-8'))
    hashed = h.hexdigest()

    guests = dict(
        ip=ip,
        is_routable=is_routable,
        user_agent=user_agent,
        updated_at=datetime.datetime.now(tz=timezone.utc),
        url_path=url_path,
        hashed_ip_agent_path=hashed,
    )
    NetworkVisitorsAddresses.objects.update_or_create(
        hashed_ip_agent_path=guests.get('hashed_ip_agent_path'),
        defaults=guests,
    )


urlpatterns = [
    path('403/', permission_denied_view),
]

handler403 = response_error_handler


# ROOT_URLCONF must specify the module that contains handler403 = ...
@override_settings(ROOT_URLCONF=__name__)
class CustomErrorHandlerTests(SimpleTestCase):

    def test_handler_renders_template_response(self):
        response = self.client.get('/403/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Error handler content', status_code=403)
