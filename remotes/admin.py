import logging

from django.contrib import admin

from remotes.models import *

log = logging.getLogger("core")


# admin.site.register(Options)

class PerlCamerasAdminInline(admin.TabularInline):
    model = PerlCameras


# admin.site.register(Class, ClassAdmin)


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
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
class PerlCamerasAdmin(admin.ModelAdmin):
    # fields = [
    #     'dvr',
    #     'cam',
    #     'type',
    #     'description',
    #     'button',
    # ]
    list_display = (
        'dvr',
        'cam',
        'type',
        'description',
        'get_button',
    )
    list_filter = (
        'dvr',
        'type',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('button')

    def get_button(self, obj):
        return ",".join([p.description for p in obj.button.all()])


@admin.register(PerlButtons)
class PerlButtonsAdmin(admin.ModelAdmin):
    list_display = (
        'dom',
        'gate',
        'mode',
        'description',
        'camera',
    )
    list_filter = (
        'dom',
        'gate',
        'mode',
    )

    @admin.display(description='Assigned camera')
    def camera(self, obj):
        # Get related button if any:
        cams = PerlCameras.objects.filter(button=obj).values_list(
            'type',
            'description',
        )
        if cams:
            return list(cams)
