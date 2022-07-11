from django.contrib import admin
from main.models import NetworkVisitorsAddresses, MailsTexts

admin.site.register(MailsTexts)


@admin.register(NetworkVisitorsAddresses)
class NetworkVisitorsAddressesAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'is_routable',
        'user_agent',
        'url_path',
        'request_get_args',
        'request_post_args',
        'updated_at',
        'created_at',
    )
    list_filter = (
        'ip',
        'is_routable',
        'created_at',
        'updated_at',
        'user_agent',
        'url_path',
    )
    ordering = ('ip',)

    search_fields = (
        'ip',
        'is_routable',
        'user_agent',
        'url_path',
    )
