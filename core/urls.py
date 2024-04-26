"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from core import constants as const
from core.security import Other
from main.views import MainPage
from blog.sitemap import BlogSitemap

ADMIN_URL = Other.ADMIN_URL

handler404 = 'core.views.page_not_found_view'
handler500 = 'core.views.response_error_handler'
handler403 = 'core.views.permission_denied_view'
handler400 = 'core.views.bad_request_view'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('index/', MainPage.as_view(), name='index'),
    # Include other:
    path('main/', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('remotes/', include('remotes.urls')),
    # Built-ins
    path(f'{ADMIN_URL}/accounts/', include('django_registration.backends.activation.urls')),
    path(f'{ADMIN_URL}/accounts/', include('django.contrib.auth.urls')),
    path(f'{ADMIN_URL}/rest-auth/', include('dj_rest_auth.urls')),
    path(f'{ADMIN_URL}/api-auth/', include('rest_framework.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(f'{ADMIN_URL}/admin/', admin.site.urls),
    # WWW
    # See also: https://django-robots.readthedocs.io/en/latest/
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": {"blog": BlogSitemap}}, name="django.contrib.sitemaps.views.sitemap"),
]

# Only load on a local dev system when needed
if const.is_dev():
    # TMCE
    path('tinymce/', include('tinymce.urls')),
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
