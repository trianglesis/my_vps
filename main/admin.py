from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from main.models import NetworkVisitorsAddresses, MailsTexts, NetworkVisitorsAddressesAgentProxy, NetworkVisitorsAddressesUrlPathProxy

admin.site.register(MailsTexts)


@admin.register(NetworkVisitorsAddresses)
class NetworkVisitorsAddressesAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)

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
        # 'ip',
        'is_routable',
        'created_at',
        'updated_at',
        'user_agent',
        # 'url_path',
    )
    search_fields = (
        'ip',
        'is_routable',
        'user_agent',
        'url_path',
    )


@admin.register(NetworkVisitorsAddressesAgentProxy)
class NetworkVisitorsAddressesAgentProxyAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    search_fields = (
        'ip',
        'is_routable',
        'user_agent',
        'url_path',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'user_agent',
    )
    list_display = (
        'ip',
        'user_agent',
        'updated_at',
        'created_at',
    )

@admin.register(NetworkVisitorsAddressesUrlPathProxy)
class NetworkVisitorsAddressesUrlPathProxyAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    search_fields = (
        'ip',
        'is_routable',
        'user_agent',
        'url_path',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'url_path',
    )
    list_display = (
        'ip',
        'url_path',
        'request_get_args',
        'request_post_args',
        'updated_at',
        'created_at',
    )