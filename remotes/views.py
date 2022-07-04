import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

log = logging.getLogger("views")


class MainPage(TemplateView):
    template_name = 'main/main_body.html'
    context_object_name = 'objects'

    # Do not show anything if user is not from family group.

