from django.urls import path

from remotes.views import *

urlpatterns = [
    # Home
    path('', MainPageRemotes.as_view(), name='remotes'),
    # Mobile view simple:
    path('mobile', RemotesMobile.as_view(), name='remotes_mobile'),

    path('web', RemotesWeb.as_view(), name='remotes_web'),
    path('cams', RemotesAllCameras.as_view(), name='remotes_cams'),
    # path('remotes/', MainPageRemotes.as_view(), name='remotes'),
]
