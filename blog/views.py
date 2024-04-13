import logging

from django.views.generic import ListView

from blog.models import Post

log = logging.getLogger("core")


class MainPageBlogListView(ListView):
    __url_path = '/blog/'
    model = Post
    template_name = 'blog.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(MainPageBlogListView, self).get_context_data(**kwargs)
        context.update(
            DEBUG=True,
        )
        return context