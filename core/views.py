import logging

from django.http import HttpResponse
from django.urls import path

from main.tasks import save_visit_task

log = logging.getLogger("core")

"""
Conf https://github.com/un33k/django-ipware
"""


def response_error_handler(request, exception=None):
    status = 500
    save_visit_task(request, status=status)
    resp = 'I dont want to.\n500 Internal Server Error'
    return HttpResponse(resp, status=status)


def page_not_found_view(request, exception=None):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/redirects/
    :param request:
    :param exception:
    :return:
    """
    status = 404
    save_visit_task(request, status=status)
    resp = f'404 Not Found'
    log.debug(f"404: {resp}")
    return HttpResponse(resp, status=status)


def bad_request_view(request, exception=None):
    """
    https://docs.djangoproject.com/en/5.0/ref/contrib/redirects/
    :param request:
    :param exception:
    :return:
    """
    status = 400
    save_visit_task(request, status=status)
    resp = "Bad request: 400"
    return HttpResponse(resp, status=status)


def permission_denied_view(request, exception=None):
    status = 403
    save_visit_task(request, status=status)
    resp = "HTTP/9.99 403 Forbidden"
    return HttpResponse(resp, status=status)

#
# urlpatterns = [
#     path('403/', permission_denied_view),
# ]
#
# handler403 = response_error_handler
