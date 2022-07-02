from django.urls import path

from main.views import *

urlpatterns = [
    # Home
    path('home/', MainPage.as_view(), name='home'),
]
