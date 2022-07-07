import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.renderers import JSONRenderer
# from rest_framework.response import Response
# from rest_framework.views import APIView


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
        context.update(
            content='Here show and choose some modules',
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        role = self.request.GET.get('role', None)
        title = 'Камеры'
        cams = PerlCameras.objects.all()
        if role:
            if role == 'candle_lo':
                cams = PerlCameras.objects.filter(type__in=[
                    'candle_1',
                    'candle_2',
                    'candle_3',
                    'candle_4',
                ])
                title = 'Свеча нижний ур'
            elif role == 'candle_up':
                cams = PerlCameras.objects.filter(type__in=[
                    'candle_5',
                    'candle_6',
                ])
                title = 'Свеча верхний ур'
            elif role == 'sport':
                cams = PerlCameras.objects.filter(type__in=[
                    'sport_1',
                    'sport_2',
                    'sport_3',
                ])
                title = 'Спортплощадка'
            elif role == 'inner':
                cams = PerlCameras.objects.filter(type__in=[
                    'inner_1',
                    'inner_2',
                ])
                title = 'Внутренний двор'
            elif role == 'outer':
                cams = PerlCameras.objects.filter(type__in=[
                    'outer_1',
                ])
                title = 'Внешний двор'

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
        role = self.request.GET.get('role', None)
        title = 'Камеры'
        if role:
            if role == 'candle_lo':
                cams = PerlCameras.objects.filter(type__in=[
                    'candle_1',
                    'candle_2',
                    'candle_3',
                    'candle_4',
                ])
                title = 'Свеча нижний ур'
            elif role == 'candle_up':
                cams = PerlCameras.objects.filter(type__in=[
                    'candle_5',
                    'candle_6',
                ])
                title = 'Свеча верхний ур'
            elif role == 'sport':
                cams = PerlCameras.objects.filter(type__in=[
                    'sport_1',
                    'sport_2',
                    'sport_3',
                ])
                title = 'Спортплощадка'
            elif role == 'inner':
                cams = PerlCameras.objects.filter(type__in=[
                    'inner_1',
                    'inner_2',
                ])
                title = 'Внутренний двор'
            elif role == 'outer':
                cams = PerlCameras.objects.filter(type__in=[
                    'outer_1',
                ])
                title = 'Внешний двор'

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


# # Operations:
# @method_decorator(login_required, name='dispatch')
# class TestCaseRunTestREST(APIView):
#     __url_path = '/octo_tku_patterns/test_execute_web/'
#     __url_path_alt = '/octo_tku_patterns/user_test_add/'
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get(self, request=None):
#         task_id = self.request.GET.get('task_id', None)
#         # log.debug("<=TestCaseRunTestREST=> GET - retrieve task by task_id: %s", task_id)
#         # log.debug("task id by request: %s", task_id)
#         # Get task status from celery-app
#         if not task_id:
#             help_ = dict(
#                 doc="Run task 't_test_prep'. Task params can be: case_id, pattern_folder_names, change, "
#                     "change_user, change_review, change_ticket, test_py_path. "
#                     "Test modes: test_wipe_run, test_p4_run, test_instant_run"
#             )
#             return Response(help_)
#
#         tasks = CeleryTaskmeta.objects.filter(task_id__exact=task_id)
#         if tasks:
#             serializer = CeleryTaskShortSerializer(tasks)
#             return Response(serializer.data)
#         else:
#             res = AsyncResult(task_id)
#             task_res = dict(
#                 # task_id=task_id,
#                 status=res.status,
#                 # result=res.result,
#                 state=res.state,
#                 # args=res.args,
#             )
#             # log.debug("Task result: %s", task_res)
#             return Response([task_res])
#
#     def post(self, request=None):
#         selector = compose_selector(self.request.data)
#         # json_ = {"tkn_branch": "tkn_main", "pattern_library": "CORE", "pattern_folder_name": "10genMongoDB", "refresh": "1"}
#         if any(value for value in selector.values()):
#             pass
#         else:
#             return Response(dict(task_id=f'Cannot run test without any selection {selector}'))
#
#         obj = dict(
#             context=dict(selector=selector),
#             request=self.request.data,
#             user_name=self.request.user.username,  # Additionally try to send email to adprod user too!
#         )
#         # TaskPrepare(obj).run_tku_patterns()
#         t_tag = f'tag=t_test_prep;user_name={self.request.user.username};'
#         t_queue = 'w_routines@tentacle.dq2'
#         t_routing_key = 'routines.TRoutine.t_test_prep'
#         task_added = TPatternRoutine.t_test_prep.apply_async(
#             args=[t_tag],
#             kwargs=dict(obj=obj),
#             queue=t_queue,
#             routing_key=t_routing_key,
#         )
#         return Response(dict(task_id=task_added.id))
