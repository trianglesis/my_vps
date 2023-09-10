import logging
import socket

import requests

from core import security

from django.views.generic import TemplateView
from django.db.models import Q
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin

from core.helpers.mailing import Mails
from remotes.tasks import RemotesTasks

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from remotes.models import PerlCameras, Options, PerlButtons

log = logging.getLogger("core")


def cam_filter(role):
    cams = PerlCameras.objects.all()
    title = 'Камеры'
    if role:
        if role == 'all':
            cams = PerlCameras.objects.filter(
                ~Q(type__istartswith='parking_cam') &
                ~Q(type__exact='Remzona') &
                ~Q(type__exact='STO_Zaezd')
            )
        elif role == 'candle_lo':
            cams = PerlCameras.objects.filter(type__in=[
                'candle_1',
                'candle_2',
                'candle_3',
                'candle_4',
            ]).order_by('type')
            title = 'Свеча нижний ур'
        elif role == 'candle_up':
            cams = PerlCameras.objects.filter(type__in=[
                'candle_5',
                'candle_6',
                'candle_7',
            ]).order_by('type')
            title = 'Свеча верхний ур'
        elif role == 'sport':
            cams = PerlCameras.objects.filter(type__in=[
                'sport_1',
                'sport_2',
                'sport_3',
                'sport_4',
            ]).order_by('type')
            title = 'Спортплощадка'
        elif role == 'inner':
            cams = PerlCameras.objects.filter(type__in=[
                'inner_1',
                'inner_2',
                'inner_3',
            ]).order_by('type')
            title = 'Внутренний двор'
        elif role == 'outer':
            cams = PerlCameras.objects.filter(type__in=[
                'outer_1',
                'outer_2',
            ]).order_by('type')
            title = 'Внешний двор'
        elif role == 'parking':
            cams = PerlCameras.objects.filter(type__istartswith="parking_cam").order_by('type')
            title = 'Парковка'
    else:
        cams = PerlCameras.objects.filter(
            ~Q(type__istartswith='parking_cam') &
            ~Q(type__exact='Remzona') &
            ~Q(type__exact='STO_Zaezd')
        )
    return cams, title


def buttons_filter(gate):
    cams = PerlButtons.objects.all()
    title = 'Кнопки'
    if gate:
        if gate == 'all':
            pass
        else:
            cams = PerlButtons.objects.filter(gate__exact=gate)
    return cams, title


class MainPageRemotes(LoginRequiredMixin, TemplateView):
    login_url = '/404'
    __url = '/remotes/'
    template_name = 'remotes.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(MainPageRemotes, self).get_context_data(**kwargs)
        title = 'Remote'
        context.update(
            title=title,
            content='Here show and choose some modules'
        )
        return context


class RemotesMobile(LoginRequiredMixin, TemplateView):
    template_name = 'mobile/mobile.html'
    context_object_name = 'objects'
    __url = 'remotes/mobile'

    def get_context_data(self, **kwargs):
        context = super(RemotesMobile, self).get_context_data(**kwargs)
        context.update(
            content='Here show and choose some modules',
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        role = self.request.GET.get('role', None)
        cams, title = cam_filter(role)

        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        perl_token = Options.objects.get(option_key__exact='bearer_token').option_value

        # Check if cameras are ON:
        cameras_off = False
        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        URL = f'{perl_hostname}/app/cam.php?dvr=1&cam=1'
        r = requests.get(URL)
        if r.status_code == 404:
            log.error(f"Cams are offline: {r}")
            cameras_off = True


        queryset = dict(
            title=title,
            role=role,
            cameras=cams,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
            cameras_off=cameras_off,

        )
        return queryset


class RemotesWeb(LoginRequiredMixin, TemplateView):
    login_url = '/404'
    __url = 'remotes/web'
    template_name = 'webacc/general.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(RemotesWeb, self).get_context_data(**kwargs)
        title = 'Cameras and buttons'
        context.update(
            title=title,
            content='Here show and choose some modules',
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        role = self.request.GET.get('role', None)
        cams, title = cam_filter(role)

        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        perl_token = Options.objects.get(option_key__exact='bearer_token').option_value

        # Check if cameras are ON:
        cameras_off = False
        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        URL = f'{perl_hostname}/app/cam.php?dvr=1&cam=1'
        r = requests.get(URL)
        if r.status_code == 404:
            log.error(f"Cams are offline: {r}")
            cameras_off = True


        queryset = dict(
            title=title,
            role=role,
            cameras=cams,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
            cameras_off=cameras_off,
        )
        return queryset


class RemotesAllCameras(LoginRequiredMixin, TemplateView):
    login_url = '/404'
    __url_path = '/remotes/cams/'
    template_name = 'webacc/all_cameras.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(RemotesAllCameras, self).get_context_data(**kwargs)
        title = 'View all cameras'
        context.update(
            title=title,
            content='Here show and choose some modules',
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        cams = PerlCameras.objects.all()
        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value

        queryset = dict(
            cameras=cams,
            perl_hostname=perl_hostname,
        )
        return queryset


class RemotesAllButtons(LoginRequiredMixin, TemplateView):
    login_url = '/404'
    __url_path = '/remotes/btns/'
    template_name = 'webacc/all_buttons.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(RemotesAllButtons, self).get_context_data(**kwargs)
        title = 'All buttons'
        context.update(
            title=title,
            content='Here show and choose some modules',
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        gate = self.request.GET.get('gate', None)
        btns, title = buttons_filter(gate)
        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        perl_token = Options.objects.get(option_key__exact='bearer_token').option_value
        queryset = dict(
            buttons=btns,
            title=title,
            gate=gate,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
        )
        return queryset


# Operations:
class OpenButtonREST(LoginRequiredMixin, APIView):
    login_url = '/404'
    __url_path = '/remotes/remote_open/'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request=None):
        return Response(dict(message='This should be POST!'))

    def post(self, request=None):
        """
        Hack to popen doors
        # {'color': '#00FF00', 'status': 'ok', 'text': '*Выполняется*', 'new_nonce': 'dslfkjhsdlkjfhsadlkjfh'}

        :param request:
        :return:
        """
        dom = self.request.data.get('dom', None)
        gate = self.request.data.get('gate', None)
        mode = self.request.data.get('mode', None)

        fake = self.request.data.get('fake', False)
        snap = self.request.data.get('snap', False)

        if socket.getfqdn() == security.DEV_HOST:
            fake = True

        kwargs_d = dict(
            username=self.request.user.username,
            send_to=self.request.user.email,
            dom=dom,
            gate=gate,
            mode=mode,
            snap=snap,
            fake=fake,
        )

        if fake:
            log.debug(f"View request: {self.request} data: {self.request.data}")
            log.info(f"FAKE ITERATION! Do not making any requests!")
            log.info(f"self.request.user.username: {self.request.user.username}, email: {self.request.user.email}")
            t_tag = f'tag=SnapOnOpening;user_name={self.request.user.username};fake_run=True'
            task_added = RemotesTasks.t_make_snap_on_open.apply_async(
                args=[t_tag],
                kwargs=kwargs_d,
            )
            j_txt = {"color": '#00FF00', "status": 'ok', "text": '*Выполняется*', "new_nonce": '00000000000000000000'}
            return Response(dict(status='Faked!', response=j_txt, task_id=task_added.id))
        # Only make a camera shot - DEPRECATED
        elif snap:
            log.info(f"Make a selfie on camera! Do not open any gate.")
            t_tag = f'tag=SnapOnOpening;user_name={self.request.user.username};snap=True;DEPRECATED'
            task_added = RemotesTasks.t_make_snap_on_open.apply_async(
                args=[t_tag],
                kwargs=kwargs_d,
            )
            return Response(dict(status='Smile!', response='Make a shot!', task_id=task_added.id))
        else:
            button = PerlButtons.objects.get(
                dom__exact=dom,
                gate__exact=gate,
                mode__exact=mode
            )
            perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
            nonce = Options.objects.get(option_key__exact='bearer_token').option_value
            URL = f'{perl_hostname}go.php?dom={dom}&gate={gate}&mode={mode}&nonce={nonce}'
            r = requests.get(URL)

            if r.status_code == 200:
                j_txt = r.json()
                server_response_status = j_txt.get("status")
                if server_response_status == 'ok':
                    # Here the task to make a snap during doors opening.
                    t_tag = f'tag=SnapOnOpening;user_name={self.request.user.username};'
                    task_added = RemotesTasks.t_make_snap_on_open.apply_async(
                        args=[t_tag],
                        kwargs=kwargs_d,
                    )
                    log.info(f"Request successfully executed for: dom={dom}&gate={gate}&mode={mode},\nResponse: {r.text}")
                    return Response(dict(status='Open!', response=j_txt, task_id=task_added.id))
                else:
                    msg = f"Request executed with some error on server side for: dom={dom}&gate={gate}&mode={mode},\nResponse: {r.text}"
                    log.error(msg)
                    body = f'User "{self.request.user.username}" open: "{button.description}"\ndom - {dom}\ngate - {gate}\nmode - {mode}\n\n{msg}'
                    Mails().short(subject=body, body=body, send_to=self.request.user.email, bcc=security.mails['admin'])
                    return Response(dict(status='Error!', response=j_txt))
            else:
                msg = f"Something is not working on server side for: dom={dom}&gate={gate}&mode={mode},\nStatus code: {r.status_code}\nResponse: {r.text}"
                log.error(msg)
                body = f'User "{self.request.user.username}" open: "{button.description}"\ndom - {dom}\ngate - {gate}\nmode - {mode}\n\n{msg}'
                Mails().short(subject=body, body=body, send_to=self.request.user.email, bcc=security.mails['admin'])
                return Response(dict(status='Error!', response=r.text, code=r.status_code))


# Operations:
class CameraShotREST(LoginRequiredMixin, APIView):
    login_url = '/404'
    __url_path = '/remotes/remote_camera_shot/'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request=None):
        return Response(dict(message='This should be POST!'))

    def post(self, request=None):
        dvr = self.request.data.get('dvr', None)
        cam = self.request.data.get('cam', None)
        log.info(f"Make a selfie on camera! Do not open any gate.")
        kwargs_d = dict(
            username=self.request.user.username,
            send_to=self.request.user.email,
            dvr=dvr,
            cam=cam,
            snap=True,
        )
        t_tag = f'tag=SnapJustNow;user_name={self.request.user.username};'
        task_added = RemotesTasks.t_make_snap_on_open.apply_async(
            args=[t_tag],
            kwargs=kwargs_d,
        )
        return Response(dict(status='Smile!', response='Make a shot!', task_id=task_added.id))
