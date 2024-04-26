import logging

from django.http import HttpResponse
from django.urls import path

from main.tasks import save_visit_task

log = logging.getLogger("core")

"""
Conf https://github.com/un33k/django-ipware
"""


def response_error_handler(request, exception=None):
    save_visit_task(request)
    resp = 'I dont want to.\n500 Internal Server Error'
    return HttpResponse(resp, status=500)


def page_not_found_view(request, exception=None):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/redirects/
    :param request:
    :param exception:
    :return:
    """
    save_visit_task(request)
    resp = f'404 Not Found'
    return HttpResponse(resp, status=404)


def bad_request_view(request, exception=None):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/redirects/
    :param request:
    :param exception:
    :return:
    """
    save_visit_task(request)
    resp = "Bad request: 400"
    return HttpResponse(resp, status=400)

def permission_denied_view(request, exception=None):
    save_visit_task(request)
    resp = "HTTP/9.99 403 Forbidden"
    return HttpResponse(resp, status=403)


urlpatterns = [
    path('403/', permission_denied_view),
]

handler403 = response_error_handler
