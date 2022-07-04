import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

log = logging.getLogger("core")


class MainPageBlog(TemplateView):
    template_name = 'blog.html'
    context_object_name = 'objects'


