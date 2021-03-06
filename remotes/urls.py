from django.urls import path

from remotes.views import *

urlpatterns = [
    # Home
    path('', MainPageRemotes.as_view(), name='remotes'),
    # Mobile view simple:
    path('mobile', RemotesMobile.as_view(), name='remotes_mobile'),

    path('web', RemotesWeb.as_view(), name='remotes_web'),
    path('cams', RemotesAllCameras.as_view(), name='remotes_cams'),
    path('btns', RemotesAllButtons.as_view(), name='remotes_buttons'),
    # path('remotes/', MainPageRemotes.as_view(), name='remotes'),

    # REST:
    path('remote_open/', OpenButtonREST.as_view(), name='remote_open'),
    path('remote_camera_shot/', CameraShotREST.as_view(), name='remote_camera_shot'),
]
