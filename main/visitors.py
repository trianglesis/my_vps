import datetime
import logging
from hashlib import blake2b
from django.utils import timezone
from ipware import get_client_ip
from main.models import NetworkVisitorsAddresses

log = logging.getLogger("dev")


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

    # log.debug(f"Making hash: \n\t{ip_agent_path} \n\thashed: {hashed}")
    # log.debug(f"Path requested: {path}")

    guests = dict(
        ip=client_ip,
        is_routable=is_routable,
        user_agent=u_agent,
        updated_at=datetime.datetime.now(tz=timezone.utc),
        url_path=path,
        request_get_args=request_get_args,
        request_post_args=request_post_args,
        hashed_ip_agent_path=hashed,
    )
    NetworkVisitorsAddresses.objects.update_or_create(
        hashed_ip_agent_path=guests.get('hashed_ip_agent_path'),
        defaults=guests,
    )
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
