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
from core import constants as const


from main.views import *

handler404 = 'core.views.page_not_found_view'
handler500 = 'core.views.response_error_handler'
handler403 = 'core.views.permission_denied_view'
handler400 = 'core.views.bad_request_view'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),

    # Include other:
    path('main/', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('remotes/', include('remotes.urls')),

    # Built-ins

    path('blah-blah-blah/a-a-accounts/', include('django_registration.backends.activation.urls')),
    path('blah-blah-blah/a-a-accounts/', include('django.contrib.auth.urls')),

    path('blah-blah-blah/re-re-rest-auth/', include('dj_rest_auth.urls')),
    path('blah-blah-blah/a-a-a-api-auth/', include('rest_framework.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),

    path('blah-blah-blah/a-a-a-admin/', admin.site.urls),

    # Only load on local dev system when needed

]

if const.is_dev():
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
