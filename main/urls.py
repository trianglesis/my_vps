from django.urls import path

from main.views import *

urlpatterns = [
    # Home
    path('', MainPage.as_view(), name='home'),
]
