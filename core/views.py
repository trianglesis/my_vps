import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings
from django.urls import path
from ipware import get_client_ip

log = logging.getLogger("dev")


"""
Conf https://github.com/un33k/django-ipware
"""

def response_error_handler(request, exception=None):
    client_ip, is_routable = get_client_ip(request)
    log.debug(f"Request HTTP Agent: {request.META['HTTP_USER_AGENT']}; ip: {client_ip} - {is_routable}")
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def page_not_found_view(request, exception=None):
    client_ip, is_routable = get_client_ip(request)
    log.debug(f"Request HTTP Agent: {request.META['HTTP_USER_AGENT']}; ip: {client_ip} - {is_routable}")
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def bad_request_view(request, exception=None):
    client_ip, is_routable = get_client_ip(request)
    log.debug(f"Request HTTP Agent: {request.META['HTTP_USER_AGENT']}; ip: {client_ip} - {is_routable}")
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


def permission_denied_view(request, exception=None):
    client_ip, is_routable = get_client_ip(request)
    log.debug(f"Request HTTP Agent: {request.META['HTTP_USER_AGENT']}; ip: {client_ip} - {is_routable}")
    resp = f'{"Nope<br>" * 9000}'
    return HttpResponse(resp, status=404)


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
