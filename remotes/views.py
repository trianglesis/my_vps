import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from remotes.models import PerlButtons, PerlCameras, Options

log = logging.getLogger("core")


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
        title = 'Cameras and buttons mobile'
        context.update(
            title=title,
            content='Here show and choose some modules',
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        cams = PerlCameras.objects.all()
        butt = PerlButtons.objects.all()

        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        perl_token = Options.objects.get(option_key__exact='bearer_token').option_value

        queryset = dict(
            cameras=cams,
            buttons=butt,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
        )
        return queryset


@method_decorator(login_required, name='dispatch')
class RemotesWeb(TemplateView):
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
        cams = PerlCameras.objects.all()
        butt = PerlButtons.objects.all()

        perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
        perl_token = Options.objects.get(option_key__exact='bearer_token').option_value

        queryset = dict(
            cameras=cams,
            buttons=butt,
            perl_hostname=perl_hostname,
            perl_token=perl_token,
        )
        return queryset


@method_decorator(login_required, name='dispatch')
class RemotesAllCameras(TemplateView):
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
