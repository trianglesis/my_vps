import logging
from hashlib import blake2b
import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import DatabaseError
from ipware import get_client_ip

from main.models import (NetworkVisitorsAddresses, URLPathsVisitors, UserAgentVisitors, RequestGetVisitors, RequestPostVisitors)

log = logging.getLogger("core")


def save_visit(request_d):
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

    client_ip = request_d.get('client_ip')
    is_routable = request_d.get('is_routable')
    u_agent = request_d.get('u_agent')
    path = request_d.get('path')
    request_get_args = request_d.get('request_get_args')
    request_post_args = request_d.get('request_post_args')

    ip_agent_path = f"{client_ip}-{u_agent}-{path}-{request_get_args}-{request_post_args}"
    h = blake2b(digest_size=64)
    h.update(ip_agent_path.encode('utf-8'))
    hashed = h.hexdigest()

    log.info(f"Saving: {ip_agent_path}")

    # Relations:
    rel_url_path, _ = URLPathsVisitors.objects.update_or_create(url_path=path)
    rel_user_agent, _ = UserAgentVisitors.objects.update_or_create(user_agent=u_agent)
    rel_request_get, _ = RequestGetVisitors.objects.update_or_create(request_get_args=request_get_args)
    rel_request_post, _ = RequestPostVisitors.objects.update_or_create(request_post_args=request_post_args)

    try:
        visitor, created = NetworkVisitorsAddresses.objects.update_or_create(
            # Get by this and update of nothing got.
            hashed_ip_agent_path=hashed,
            defaults=dict(
                ip=client_ip,
                is_routable=is_routable,
                rel_url_path=rel_url_path,
                rel_user_agent=rel_user_agent,
                rel_request_get=rel_request_get,
                rel_request_post=rel_request_post,
            ),
        )
        if created:
            log.info(f"Visitor: {visitor} created: {created}")

    # I forgot to handle different problems:
    except ObjectDoesNotExist as e:
         # Rare or should not happen
        exc_type, exc_value, exc_traceback = sys.exc_info()
        sam = traceback.format_exception(exc_type, exc_value, exc_traceback)
        log.error(f"Cannot update of create a visitor!"
                  f"\n\tException:\n{e}"
                  f"\n\tTraceback:\n{sam}")

    except MultipleObjectsReturned as e:
        # Rare or should not happen
        exc_type, exc_value, exc_traceback = sys.exc_info()
        sam = traceback.format_exception(exc_type, exc_value, exc_traceback)
        log.error(f"Cannot update of create a visitor!"
                  f"\n\tException:\n{e}"
                  f"\n\tTraceback:\n{sam}")

    except DatabaseError as e:
        # Happened a few times, investigating
        exc_type, exc_value, exc_traceback = sys.exc_info()
        sam = traceback.format_exception(exc_type, exc_value, exc_traceback)
        log.error(f"Cannot update of create a visitor!"
                  f"\n\tException:\n{e}"
                  f"\n\tTraceback:\n{sam}")
    return None


def pick_request_useful_data(request):
    """
    Get all data from request and pass it to a celery task asap.
    :param request:
    :return:
    """
    client_ip, is_routable = get_client_ip(request)

    request_get_args = request.GET.dict()
    if not request_get_args:
        request_get_args = None

    request_post_args = request.POST.dict()
    if not request_post_args:
        request_post_args = None

    # log.debug(f"request: {client_ip} {request.path}  {request_get_args} {request_post_args} saving")
    pickable_dict = dict(
        client_ip=client_ip,
        is_routable=is_routable,
        u_agent=request.META.get('HTTP_USER_AGENT', None),
        path=request.path,
        request_get_args=request_get_args,
        request_post_args=request_post_args,
    )
    return pickable_dict
