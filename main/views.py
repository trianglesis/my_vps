import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

log = logging.getLogger("core")


class MainPage(TemplateView):
    template_name = 'main/main_body.html'
    context_object_name = 'objects'

    # TODO: Later add here some photos I want to show with maybe lik to the post.
    # TODO: Later add random or set of recent or popular posts here

