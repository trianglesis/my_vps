from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from main.models import (NetworkVisitorsAddresses, MailsTexts,
                         NetworkVisitorsAddressesAgentProxy, NetworkVisitorsAddressesUrlPathProxy,
                         URLPathsVisitors, UserAgentVisitors, RequestGetVisitors, RequestPostVisitors,
                         Options)

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
    list_per_page = 300


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
    list_per_page = 300


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
    list_per_page = 300


@admin.register(URLPathsVisitors)
class URLPathsVisitorsAdmin(admin.ModelAdmin):
    # date_hierarchy = "created_at"  # FIX TZ for MySQL
    ordering = ["-created_at"]
    search_fields = ["url_path"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "url_path",
    ]
    readonly_fields = [
        "url_path",
        "created_at",
        "hits",
        "visitors_table",
    ]
    list_per_page = 50
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
        field = '<table style="width:100%"><tr><td>ip</td><td>updated</td><td>created</td>'
        if obj.visitor_rel_url_path:
            for visitor in obj.visitor_rel_url_path.all().order_by("-updated_at"):
                field += f"<tr><td>{visitor.ip}</td><td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td><td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>"
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(UserAgentVisitors)
class UserAgentVisitorsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["user_agent"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "user_agent",
    ]
    readonly_fields = [
        "user_agent",
        "created_at",
        "hits",
        "visitors_table",
    ]
    list_per_page = 50
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("user_agent",),
                ("created_at",),
                ("hits",),
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
            _hits_count=Count("visitor_rel_url_path__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = '<table style="width:100%"><tr><td>ip</td><td>updated</td><td>created</td>'
        if obj.visitor_rel_user_agent:
            for visitor in obj.visitor_rel_user_agent.all().order_by("-updated_at"):
                field += f"<tr><td>{visitor.ip}</td><td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td><td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>"
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(RequestGetVisitors)
class RequestGetVisitorsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["request_get_args"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "request_get_args",
    ]
    readonly_fields = [
        "request_get_args",
        "created_at",
        "hits",
        "visitors_table",
    ]
    list_per_page = 50
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("request_get_args",),
                ("created_at",),
                ("hits",),
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
            _hits_count=Count("visitor_rel_url_path__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = '<table style="width:100%"><tr><td>ip</td><td>updated</td><td>created</td>'
        if obj.visitor_rel_request_get:
            for visitor in obj.visitor_rel_request_get.all().order_by("-updated_at"):
                field += f"<tr><td>{visitor.ip}</td><td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td><td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>"
        field += '</tr></table>'
        return format_html(field)

    hits.short_description = "Hits"
    hits.admin_order_field = '_hits_count'
    visitors_table.short_description = "Visitors Table"


@admin.register(RequestPostVisitors)
class RequestPostVisitorsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["request_post_args"]
    list_filter = ["created_at"]
    list_display = [
        "pk",
        "created_at",
        "hits",
        "request_post_args",
    ]
    readonly_fields = [
        "request_post_args",
        "created_at",
        "hits",
        "visitors_table",
    ]
    list_per_page = 50
    fieldsets = [
        ('Details', {
            'description': "Basic info",
            'fields': [
                ("request_post_args",),
                ("created_at",),
                ("hits",),
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
            _hits_count=Count("visitor_rel_url_path__hashed_ip_agent_path", distinct=True),
        )
        return queryset

    def visitors_table(self, obj):
        field = '<table style="width:100%"><tr><td>ip</td><td>updated</td><td>created</td>'
        if obj.visitor_rel_request_post:
            for visitor in obj.visitor_rel_request_post.all().order_by("-updated_at"):
                field += f"<tr><td>{visitor.ip}</td><td>{visitor.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</td><td>{visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>"
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
    list_per_page = 50
