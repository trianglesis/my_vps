import logging
import typing

# from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpRequest, HttpResponse

from main.tasks import save_visit_task

log = logging.getLogger("core")


class UserVisitMiddleware:
    """Middleware to record user visits."""

    def __init__(self, get_response: typing.Callable) -> None:
        # TODO: Add Option to disable
        # if RECORDING_DISABLED:
        #     raise MiddlewareNotUsed("UserVisit recording has been disabled")
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> typing.Optional[HttpResponse]:

        # Actually save
        # TODO: Add option to skip local IP, my IP and admin browsing
        save_visit_task(request)

        if request.user.is_anonymous:
            return self.get_response(request)

        return self.get_response(request)