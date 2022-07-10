from django.contrib import admin
from main.models import NetworkVisitorsAddresses

# Register your models here.
# admin.site.unregister(User)

# DEBUG:
# admin.site.register(User)
# admin.site.register(AuthGroup)
# admin.site.register(AuthGroupPermissions)
# admin.site.register(AuthPermission)
# admin.site.register(AuthUser)
# admin.site.register(AuthUserGroups)
# admin.site.register(AuthUserUserPermissions)
# admin.site.register(DjangoAdminLog)
# admin.site.register(DjangoContentType)
# admin.site.register(DjangoMigrations)
# admin.site.register(DjangoSession)


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
