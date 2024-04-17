import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from blog.models import Post, Tag

log = logging.getLogger("core")


class MainPage(TemplateView):
    template_name = 'main/main_body.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context.update(
            debug=False,
            objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        main_data = dict(
            posts = Post.objects.all(),
            tags = Tag.objects.all(),
        )
        return main_data

