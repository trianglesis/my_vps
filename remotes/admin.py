from django.contrib import admin

from remotes.models import *


# admin.site.register(Options)


@admin.register(Options)
class RemotesOptions(admin.ModelAdmin):
    list_display = (
        'option_key',
        'option_value',
        'created_at',
        'private',
        'description',
    )
    list_filter = (
        'option_key',
        'created_at',
        'private',
    )
    ordering = ('-created_at',)
    search_fields = (
        'option_key',
        'option_value',
        'description',
    )


@admin.register(PerlCameras)
class RemotesOptions(admin.ModelAdmin):
    list_display = (
        'dvr',
        'cam',
        'type',
        'description',
        'button',
    )


@admin.register(PerlButtons)
class RemotesOptions(admin.ModelAdmin):
    list_display = (
        'dom',
        'gate',
        'mode',
        'description',
    )
