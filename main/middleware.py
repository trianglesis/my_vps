import logging
import typing

from django.core.exceptions import SuspiciousOperation
# from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render

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
        """
        Check request for validity here and response with correct answers.
        Use bad codes when needed.
        Save visitor now with status code relation.
        :param request:
        :return:
        """
        try:
            response = self.get_response(request)
        except SuspiciousOperation as e:
            log.error(f"SuspiciousOperation:"
                      f"\nException:\n{e}\n")
            response = HttpResponseForbidden('CSRF verification failed.')
        except Exception as e:
            log.error(f"General Exception: returning the main page by default."
                      f"\nException:\n{e}\n")
            save_visit_task(request, status='ERR')
            return render(request, 'main/main_body.html', {
                'error_message': 'Something went wrong!',
                'error_code': f'CODE: ERR'
            })

        # Save with status code:
        save_visit_task(request, status=response.status_code)
        # Indicate status code and errors at main page alert section
        # Redirects to the main page!
        bad_codes = [400, 401, 403, 404, 500]
        if response.status_code in bad_codes:
            return render(request, 'main/main_body.html', {
                'error_message': 'Something went wrong!',
                'error_code': f'CODE: {response.status_code}'
            })
        return response

    def process_exception(self, request, exception):
        """
        To save exception when request is not recognized
        For example,
        - Invalid HTTP_HOST header:
        :param request:
        :param exception:
        :return:
        """
        log.error(f"Middleware process_exception:\n{str(exception)}\n")