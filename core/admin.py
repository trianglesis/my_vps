import json
import pickle
from html import escape
from pprint import pformat

from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.models import *

# Register your models here.
# admin.site.unregister(User)

# DEBUG:
# admin.site.register(User)
admin.site.register(AuthGroup)
admin.site.register(AuthGroupPermissions)
admin.site.register(AuthPermission)
admin.site.register(AuthUser)
admin.site.register(AuthUserGroups)
admin.site.register(AuthUserUserPermissions)
admin.site.register(DjangoAdminLog)
admin.site.register(DjangoContentType)
admin.site.register(DjangoMigrations)
admin.site.register(DjangoSession)

# admin.site.register(CeleryTaskmeta)
admin.site.register(CeleryTasksetmeta)


@admin.register(CeleryTaskmeta)
class CeleryTaskmetaAdmin(admin.ModelAdmin):
    ordering = ('-status',)

    list_display = (
        'name',
        'task_id',
        'status',
        'worker_queue',
        # 'worker',
        # 'queue',
        'retries',
        'date_done',
    )
    list_filter = (
        'status',
        'worker',
        'queue',
        'name',
        'date_done',
    )

    readonly_fields = (
        'task_id',
        'name',
        'traceback',
        'args',
        'kwargs',
        'result',
        'worker',
        'retries',
        'queue',
        'status',
        'date_done',
    )

    list_per_page = 25

    fieldsets = [
        ('Celery task',
         {'description': "Celery task info",
          'fields': (
              ('task_id', 'name'),
              ('status', 'date_done',),
          )}),
        ('Task workers',
         {'description': "Workers and queue",
          'fields': (
              ('worker', 'queue', 'retries',),
          )}),
        ('Parameters',
         {'fields': (
             ('args',),
             ('kwargs',),
         )}),
        ('Result',
         {'fields': (
             ('result',),
         )}),
        ('Task Traceback',
         {'description': "Celery Task Traceback if any",
          'fields': (
              ('traceback',),
          )}),
    ]

    def worker_queue(self, obj):
        return format_html(f"W: {obj.worker}<br>Q: {obj.queue}")

    worker_queue.short_description = "Worker/Queue"


@admin.register(CeleryTaskmetaProxy)
class CeleryTaskmetaProxyAdmin(admin.ModelAdmin):
    list_display = (
        'name_task_id',
        'worker_queue',
        # 'name',
        # 'task_id',
        'status',
        'load_args_and_kwargs',
        # 'args_convert',
        # 'kwargs_convert',
        # 'worker',
        # 'queue',
        # 'result_convert',
        # 'retries',
        # 'date_done',
    )
    list_filter = (
        'status',
        'worker',
        'queue',
        'name',
        'date_done',
    )

    readonly_fields = (
        'task_id',
        'name',
        'traceback',
        'args',
        'kwargs',
        'result',
        'worker',
        'retries',
        'queue',
        'status',
        'date_done',
    )

    list_per_page = 5

    fieldsets = [
        ('Celery task',
         {'description': "Celery task info",
          'fields': (
              ('task_id', 'name'),
              ('status', 'date_done',),
          )}),
        ('Task workers',
         {'description': "Workers and queue",
          'fields': (
              ('worker', 'queue', 'retries',),
          )}),
        ('Parameters',
         {'fields': (
             ('args',),
             ('kwargs',),
         )}),
        ('Result',
         {'fields': (
             ('result',),
         )}),
        ('Task Traceback',
         {'description': "Celery Task Traceback if any",
          'fields': (
              ('traceback',),
          )}),
    ]

    def name_task_id(self, obj):
        return format_html(f"{obj.name}<br><br>{obj.task_id}")

    def worker_queue(self, obj):
        return format_html(f"{obj.worker}<br>{obj.queue}")

    def load_args_and_kwargs(self, obj):
        args_f = ''
        kwargs_f = ''
        if obj.args:
            _args = pickle.loads(obj.args, encoding='UTF-8')
            _args = json.dumps(_args, indent=4, ensure_ascii=False, default=pformat)
            _args = escape(_args.replace("', '", "',\n            '"))
            args_f = f"Args: {_args}"
            args_f = args_f.replace("\n", "<br>")
            args_f = args_f.replace(" ", "&nbsp;")
        if obj.kwargs:
            _kwargs = pickle.loads(obj.kwargs, encoding='UTF-8')
            _kwargs = json.dumps(_kwargs, indent=4, ensure_ascii=False, default=pformat)
            _kwargs = escape(_kwargs.replace(">,", ",\n            ").replace("<", "").replace(">", ""))
            kwargs_f = f"Kwargs: {_kwargs}"
            kwargs_f = kwargs_f.replace("\n", "<br>")
            kwargs_f = kwargs_f.replace(" ", "&nbsp;")
        # return format_html(u'{}<br><br>{}', args_f, kwargs_f)
        return mark_safe(f'{args_f}<br><br>{kwargs_f}')

    def result_convert(self, obj):
        if obj.result:
            return str(pickle.loads(obj.result))
        return ''

    load_args_and_kwargs.short_description = "args and kwargs from pickle load"
    result_convert.short_description = "Result"
    name_task_id.short_description = "Task name and ID"
    worker_queue.short_description = "Worker/Queue"

# admin.site.register(Site)
