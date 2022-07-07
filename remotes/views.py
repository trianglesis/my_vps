import logging

import requests
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Q

from core.helpers.mailing import Mails

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
        # perl_token = self.request.data.get('perl_token', None)
        perl_hostname = self.request.data.get('perl_hostname', None)

        button = PerlButtons.objects.get(dom__exact=dom, gate__exact=gate, mode__exact=mode)
        subject = f'Remote open: {button.description}'
        body = f'User "{self.request.user.username}" open: "{button.description}"\ndom - {dom}\ngate - {gate}\nmode - {mode}'

        if fake:
            log.info(f"FAKE ITERATION! Do not making any requests!")
            log.info(f"self.request.user.username: {self.request.user.username}, email: {self.request.user.email}")

            Mails().short(subject=subject, body=body, send_to=self.request.user.email, bcc='to@trianglesis.org.ua')

            j_txt = dict()
            return Response(dict(status='ok', response=j_txt))
        else:
            URL = f'https://{perl_hostname}/app/go.php?dom={dom}&gate={gate}&mode={mode}&nonce={nonce}'
            r = requests.get(URL)

            if r.status_code == 200:
                j_txt = r.json()
                server_response_status = j_txt.get("status")
                if server_response_status == 'ok':
                    # Send even if unsuccessfully - to show that user actually tries it:
                    Mails().short(subject=subject, body=body, send_to=self.request.user.email, bcc='to@trianglesis.org.ua')

                    log.info(f"Request successfully executed for: dom={dom}&gate={gate}&mode={mode},\nResponse: {r.text}")
                    return Response(dict(status='ok', response=j_txt))
                else:
                    log.error(f"Request executed with some error on server side for: dom={dom}&gate={gate}&mode={mode},\nResponse: {r.text}")
                    return Response(dict(status='err', response=j_txt))
            else:
                log.error(f"Something is not working on server side for: dom={dom}&gate={gate}&mode={mode},\nStatus code: {r.status_code}\nResponse: {r.text}")
                return Response(dict(status='err', response=r.text, code=r.status_code))
