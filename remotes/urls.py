from django.urls import path

from remotes.views import *

urlpatterns = [
    # Home
    path('', MainPageRemotes.as_view(), name='remotes'),
    # path('remotes/', MainPageRemotes.as_view(), name='remotes'),
]
