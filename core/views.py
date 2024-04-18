import datetime
import logging

from hashlib import blake2b

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.test import SimpleTestCase, override_settings
from django.urls import path
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from ipware import get_client_ip

from main.models import NetworkVisitorsAddresses

log = logging.getLogger("dev")

"""
Conf https://github.com/un33k/django-ipware
"""


def response_error_handler(request, exception=None):
    client_ip, is_routable = get_client_ip(request)
    # log.debug(f"request: {client_ip} {request.path}  {request.GET.dict()} {request.POST.dict()} saving")
    save_visit(client_ip, is_routable, request)
    resp = 'I dont want to.\n500 Internal Server Error'
    return HttpResponse(resp, status=500)


def page_not_found_view(request, exception=None):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/redirects/
    :param request:
    :param exception:
    :return:
    """
    client_ip, is_routable = get_client_ip(request)
    # log.debug(f"request: {client_ip} {request.path}  {request.GET.dict()} {request.POST.dict()} saving")
    save_visit(client_ip, is_routable, request)
    resp = f'404 Not Found'
    return HttpResponse(resp, status=404)
    # return render(request, 'main/main_body.html')


def bad_request_view(request, exception=None):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/redirects/
    :param request:
    :param exception:
    :return:
    """
    client_ip, is_routable = get_client_ip(request)
    # log.debug(f"request: {client_ip} {request.path}  {request.GET.dict()} {request.POST.dict()} saving")
    save_visit(client_ip, is_routable, request)
    resp = "Bad request: 400"
    return HttpResponse(resp, status=400)
    # return render(request, 'main/main_body.html')

def permission_denied_view(request, exception=None):
    client_ip, is_routable = get_client_ip(request)
    # log.debug(f"request: {client_ip} {request.path}  {request.GET.dict()} {request.POST.dict()} saving")
    save_visit(client_ip, is_routable, request)
    resp = "HTTP/9.99 403 Forbidden"
    return HttpResponse(resp, status=403)


def save_visit(ip, is_routable, request):
    """
    Save each visit if user got errors or tried to access some places.
    Later
        - add here check for length of request string and drop request if string is too long?
        - add IP check - if user happens to be mentioned in this table more that N times - ban.

    :param ip:
    :param is_routable:
    :param request:
    :return:
    """
    # Making unique hash for ip + user agent + path requested
    u_agent = request.META.get('HTTP_USER_AGENT', None)
    ip_agent_path = f"{ip}-{u_agent}-{request.path}-{request.GET.dict()}-{request.POST.dict()}"
    h = blake2b(digest_size=64)
    h.update(ip_agent_path.encode('utf-8'))
    hashed = h.hexdigest()
    log.debug(f"Making hash: \n\t{ip_agent_path} \n\thashed: {hashed}")

    guests = dict(
        ip=ip,
        is_routable=is_routable,
        user_agent=u_agent,
        updated_at=datetime.datetime.now(tz=timezone.utc),
        url_path=request.path,
        request_get_args=request.GET.dict(),
        request_post_args=request.POST.dict(),
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
