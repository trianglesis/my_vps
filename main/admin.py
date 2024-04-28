from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from core.security import Other

from main.models import (NetworkVisitorsAddresses, MailsTexts,
                         URLPathsVisitors, UserAgentVisitors, RequestGetVisitors, RequestPostVisitors,
                         Options)

ADMIN_URL = Other.ADMIN_URL

admin.site.register(MailsTexts)


def validate_and_escape(field):
    if field:
        field = str(field).replace("{", '').replace("}", '')
    else:
        field = ''
    return field


@admin.register(NetworkVisitorsAddresses)
class NetworkVisitorsAddressesAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)

    list_display = (
        'ip',
        'is_routable',
        'url_path_fk',
        'user_agent_fk',
        'request_get_fk',
        'request_post_fk',
        'updated_at',
        'created_at',
    )
    readonly_fields = (
        'ip',
        'is_routable',
        'url_path_fk',
        'user_agent_fk',
        'request_get_fk',
        'request_post_fk',
        'updated_at',
        'created_at',
    )
    list_filter = (
        'is_routable',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'ip',
    )
    list_per_page = 25
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ('ip', 'is_routable',),
                ('updated_at', 'created_at',),
            ]
        }),
        ('Relations', {
            'description': "Basic info",
            'fields': [
                ('url_path_fk',),
                ('user_agent_fk',),
                ('request_get_fk',),
                ('request_post_fk',),
            ]
        })
    ]

    def url_path_fk(self, obj):
        if obj.rel_url_path:
            return obj.rel_url_path.url_path

    def user_agent_fk(self, obj):
        if obj.rel_user_agent:
            return obj.rel_user_agent.user_agent

    def request_get_fk(self, obj):
        if obj.rel_request_get:
            return obj.rel_request_get.request_get_args

    def request_post_fk(self, obj):
        if obj.rel_request_post:
            return obj.rel_request_post.request_post_args

    url_path_fk.short_description = 'url_path'
    user_agent_fk.short_description = 'user_agent'
    request_get_fk.short_description = 'request_get'
    request_post_fk.short_description = 'request_post'


@admin.register(URLPathsVisitors)
class URLPathsVisitorsAdmin(admin.ModelAdmin):
    # date_hierarchy = "created_at"  # FIX TZ for MySQL
    ordering = ["-created_at"]
    search_fields = ["url_path", "hash"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "hash",
        "url_path",
    ]
    readonly_fields = [
        "url_path",
        "created_at",
        "hits",
        "hash",
        "visitors_table",
    ]
    list_per_page = 25
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("url_path",),
                ("created_at",),
                ("hits",),
                ("visitors_table",),
            ]
        })
    ]

    def hits(self, obj):
        value = 0
        if obj.visitor_rel_url_path:
            return obj.visitor_rel_url_path.all().count()
        return value

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hits_count=Count("visitor_rel_url_path__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = ('<table style="width:100%">'
                 '<tr>'
                 '<td>ip</td>'
                 '<td>updated</td>'
                 '<td>created</td>'
                 '<td>get</td>'
                 '<td>post</td>'
                 '')
        if obj.visitor_rel_url_path:
            for visitor in obj.visitor_rel_url_path.all().order_by("-updated_at"):
                field += (f"<tr>"
                          f"<td><a href=/{ADMIN_URL}/admin/main/networkvisitorsaddresses/{visitor.id}/change/>{visitor.ip}<a></td>"
                          f"<td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{validate_and_escape(visitor.rel_request_get.request_get_args)}</td>"
                          f"<td>{validate_and_escape(visitor.rel_request_post.request_post_args)}</td>"
                          f"</tr>")
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(UserAgentVisitors)
class UserAgentVisitorsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["user_agent", "hash"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "hash",
        "user_agent",
    ]
    readonly_fields = [
        "user_agent",
        "created_at",
        "hits",
        "hash",
        "visitors_table",
    ]
    list_per_page = 25
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("user_agent",),
                ("created_at",),
                ("hits",),
                ("hash",),
                ("visitors_table",),
            ]
        })
    ]

    def hits(self, obj):
        value = ""
        if obj.visitor_rel_user_agent:
            value = obj.visitor_rel_user_agent.all().count()
        return value

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hits_count=Count("visitor_rel_user_agent__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = ('<table style="width:100%">'
                 '<tr>'
                 '<td>ip</td>'
                 '<td>updated</td>'
                 '<td>created</td>'
                 '<td>url</td>'
                 '<td>get</td>'
                 '<td>post</td>'
                 '')
        if obj.visitor_rel_user_agent:
            for visitor in obj.visitor_rel_user_agent.all().order_by("-updated_at"):
                field += (f"<tr>"
                          f"<td><a href=/{ADMIN_URL}/admin/main/networkvisitorsaddresses/{visitor.id}/change/>{visitor.ip}<a></td>"
                          f"<td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.rel_url_path.url_path if visitor.rel_url_path.url_path else ''}</td>"
                          f"<td>{validate_and_escape(visitor.rel_request_get.request_get_args)}</td>"
                          f"<td>{validate_and_escape(visitor.rel_request_post.request_post_args)}</td>"
                          f"</tr>")
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(RequestGetVisitors)
class RequestGetVisitorsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["request_get_args", "hash"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "hash",
        "request_get_args",
    ]
    readonly_fields = [
        "request_get_args",
        "created_at",
        "hits",
        "hash",
        "visitors_table",
    ]
    list_per_page = 25
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("request_get_args",),
                ("created_at",),
                ("hits",),
                ("hash",),
                ("visitors_table",),
            ]
        })
    ]

    def hits(self, obj):
        value = ""
        if obj.visitor_rel_request_get:
            value = obj.visitor_rel_request_get.all().count()
        return value

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hits_count=Count("visitor_rel_request_get__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = ('<table style="width:100%">'
                 '<tr>'
                 '<td>ip</td>'
                 '<td>updated</td>'
                 '<td>created</td>'
                 '<td>url</td>'
                 '')
        if obj.visitor_rel_request_get and obj.visitor_rel_request_get.all():
            for visitor in obj.visitor_rel_request_get.all().order_by("-updated_at"):
                field += (f"<tr>"
                          f"<td><a href=/{ADMIN_URL}/admin/main/networkvisitorsaddresses/{visitor.id}/change/>{visitor.ip}<a></td>"
                          f"<td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.rel_url_path.url_path if visitor.rel_url_path.url_path else ''}</td>"
                          f"</tr>")
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(RequestPostVisitors)
class RequestPostVisitorsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["request_post_args", "hash"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "hash",
        "request_post_args",
    ]
    readonly_fields = [
        "request_post_args",
        "created_at",
        "hits",
        "hash",
        "visitors_table",
    ]
    list_per_page = 25
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("request_post_args",),
                ("created_at",),
                ("hits",),
                ("hash",),
                ("visitors_table",),
            ]
        })
    ]

    def hits(self, obj):
        value = ""
        if obj.visitor_rel_request_post:
            value = obj.visitor_rel_request_post.all().count()
        return value

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hits_count=Count("visitor_rel_request_post__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = ('<table style="width:100%">'
                 '<tr>'
                 '<td>ip</td>'
                 '<td>updated</td>'
                 '<td>created</td>'
                 '<td>url</td>'
                 '')
        if obj.visitor_rel_request_post:
            for visitor in obj.visitor_rel_request_post.all().order_by("-updated_at"):
                field += (f"<tr>"
                          f"<td><a href=/{ADMIN_URL}/admin/main/networkvisitorsaddresses/{visitor.id}/change/>{visitor.ip}<a></td>"
                          f"<td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td>"
                          f"<td>{visitor.rel_url_path.url_path if visitor.rel_url_path.url_path else ''}</td>"
                          f"</tr>")
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    search_fields = (
        'option_key',
        'option_value',
        'comments',
    )
    list_filter = (
        'option_bool',
        'private',
        'created_at',
        'updated_at',
    )
    list_display = (
        'option_key',
        'option_value',
        'option_bool',
        'private',
        'comments',
        'created_at',
        'updated_at',
    )
    list_per_page = 25
