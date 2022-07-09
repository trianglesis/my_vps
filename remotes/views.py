import logging
import socket
from time import sleep

import requests
import PIL
from PIL import Image
import io
from core import security

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Q
from django.template import loader

from core.helpers.mailing import Mails

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from remotes.models import PerlCameras, Options, PerlButtons

log = logging.getLogger("core")

skip_words = [
    'Forbidden',
    'Unauthorized',
    'HTTP/1.0 500',
    'HTTP/1.0 404',
    'Fatal error',
    'HTTP request failed',
]


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


def request_image(cam_url, caller='nobody'):
    log.debug(f"2.0 Requesting image content by url: {cam_url} by: {caller}")
    r = requests.get(cam_url)
    if r.status_code == 200:
        if not any(elem in r.text for elem in skip_words):
            if r.content:
                log.debug(f"2.1 Successful request pic URL: {cam_url}")
                return r.content
    log.debug(f"2.2 Unsuccessful request pic URL: {cam_url}, will return empty bytecode and retry")
    return b''


def save_image(runs, cam_url, images, content, basewidth=600):
    stop = 3
    runs += 1
    log.debug(f"3.1 Save image attempt: {runs}")
    if runs > stop:
        log.debug(f"3.4 Last attempt to save image: {runs} full stop at: {stop}")
        pass
    else:
        img_bytes = io.BytesIO(content)
        try:
            log.debug(f"3.2 Save image attempt: {runs} try save!")
            image = PIL.Image.open(img_bytes).convert("RGB")
            wpercent = (basewidth / float(image.width))
            hsize = int((float(image.height) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)
            images.append(image)
        except PIL.UnidentifiedImageError as e:
            sleep(0.5)
            log.error(f"3.3 Cannot save image: {cam_url}, attempt: {runs}, Exception caught: {e}")
            content = request_image(cam_url, caller=f'exception, run:{runs}')
            save_image(runs, cam_url, images, content, basewidth)


def camera_shot(button, perl_hostname, basewidth=600):
    images = []
    if button.assigned_buttons.all():
        for camera in button.assigned_buttons.all():
            runs = 0
            # cam_url = f"{perl_hostname}cam.php?dvr=12&cam=47"
            cam_url = f"{perl_hostname}cam.php?dvr={camera.dvr}&cam={camera.cam}"
            log.debug(f"1.0 Requesting camera content: {cam_url}")
            content = request_image(cam_url, caller='initial')
            log.debug(f"3.0 Save image or check if save-able content: {cam_url}")
            save_image(runs, cam_url, images, content, basewidth)
            log.debug(f"4.0 Finishing job for this image and run forward! {cam_url}")
    return images


@method_decorator(login_required, name='dispatch')
class MainPageRemotes(TemplateView):
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


@method_decorator(login_required, name='dispatch')
class RemotesMobile(TemplateView):
    template_name = 'mobile/mobile.html'
    context_object_name = 'objects'

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

        queryset = dict(
            title=title,
            role=role,
            cameras=cams,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
        )
        return queryset


@method_decorator(login_required, name='dispatch')
class RemotesWeb(TemplateView):
    __url = '/remotes/web/'
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

        queryset = dict(
            title=title,
            role=role,
            cameras=cams,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
        )
        return queryset


@method_decorator(login_required, name='dispatch')
class RemotesAllCameras(TemplateView):
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


@method_decorator(login_required, name='dispatch')
class RemotesAllButtons(TemplateView):
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
@method_decorator(login_required, name='dispatch')
class TestCaseRunTestREST(APIView):
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
        nonce = self.request.data.get('nonce', None)
        fake = self.request.data.get('fake', None)
        snap = self.request.data.get('snap', None)
        # perl_token = self.request.data.get('perl_token', None)
        perl_hostname = self.request.data.get('perl_hostname', None)

        pushed_button = loader.get_template('emails/pushed_button.html')
        button = PerlButtons.objects.get(dom__exact=dom, gate__exact=gate, mode__exact=mode)

        subject = f'Remote open: {button.description}'

        if socket.getfqdn() == security.DEV_HOST:
            fake = False

        if fake:
            subject = f'Fake open: {button.description}'
            log.info(f"FAKE ITERATION! Do not making any requests!")
            log.info(f"self.request.user.username: {self.request.user.username}, email: {self.request.user.email}")
            images = camera_shot(button, perl_hostname)
            mail_html = pushed_button.render(dict(
                subject=subject,
                button=button,
                username=self.request.user.username,
                hostname=security.Credentials.SITE,
            ))
            Mails().short(
                subject=subject,
                mail_html=mail_html,
                images=images,
                send_to=self.request.user.email,
                bcc=security.mails['admin'],
            )
            j_txt = dict()
            return Response(dict(status='Faked!', response=j_txt))
        # Only make a camera shot
        elif snap:

            log.info(f"Make a selfie on camera! Do not open any gate.")
            log.debug(f"View request: {self.request} data: {self.request.data}")

            subject = f'Remote snapshot: {button.description}'
            maked_snap = loader.get_template('emails/maked_snap.html')
            images = camera_shot(button, perl_hostname, 1200)
            mail_html = maked_snap.render(dict(
                subject=subject,
                button=button,
                username=self.request.user.username,
                hostname=security.Credentials.SITE,
            ))
            # log.debug(f"images: {images}")
            Mails().short(
                subject=subject,
                mail_html=mail_html,
                images=images,
                send_to=self.request.user.email,
                bcc=security.mails['admin'],
            )
            return Response(dict(status='Smile!', response='Make a shot!'))
        else:
            URL = f'{perl_hostname}go.php?dom={dom}&gate={gate}&mode={mode}&nonce={nonce}'
            r = requests.get(URL)

            if r.status_code == 200:
                j_txt = r.json()
                server_response_status = j_txt.get("status")
                if server_response_status == 'ok':
                    images = camera_shot(button, perl_hostname, 1200)
                    mail_html = pushed_button.render(dict(
                        subject=subject,
                        button=button,
                        username=self.request.user.username,
                    ))
                    Mails().short(
                        subject=subject,
                        mail_html=mail_html,
                        images=images,
                        send_to=self.request.user.email,
                        bcc=security.mails['admin'],
                    )

                    log.info(f"Request successfully executed for: dom={dom}&gate={gate}&mode={mode},\nResponse: {r.text}")
                    return Response(dict(status='Open!', response=j_txt))
                else:
                    msg = f"Request executed with some error on server side for: dom={dom}&gate={gate}&mode={mode},\nResponse: {r.text}"
                    log.error(msg)
                    body = f'User "{self.request.user.username}" open: "{button.description}"\ndom - {dom}\ngate - {gate}\nmode - {mode}\n\n{msg}'
                    Mails().short(subject=subject, body=body, send_to=self.request.user.email, bcc=security.mails['admin'])
                    return Response(dict(status='Error!', response=j_txt))
            else:
                msg = f"Something is not working on server side for: dom={dom}&gate={gate}&mode={mode},\nStatus code: {r.status_code}\nResponse: {r.text}"
                log.error(msg)
                body = f'User "{self.request.user.username}" open: "{button.description}"\ndom - {dom}\ngate - {gate}\nmode - {mode}\n\n{msg}'
                Mails().short(subject=subject, body=body, send_to=self.request.user.email, bcc=security.mails['admin'])
                return Response(dict(status='Error!', response=r.text, code=r.status_code))
