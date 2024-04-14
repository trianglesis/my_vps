import logging

from django.core.exceptions import FieldError
from django.views.generic import ListView, DetailView

from blog.models import Post

log = logging.getLogger("core")


def blog_selector(request_GET):
    """
    :param request_GET:  self.request.GET
    :return: dict of evaluated query values
    """
    selector = dict(
        tag=request_GET.get('tag', None),
    )
    validated = {key: value for key, value in selector.items() if value and value is not None}
    return validated


def blog_filer(selector, queryset):
    """
    Return filtered items.
    :param selector: dict from blog_selector
    :param queryset: queryset from View
    :return:
    """
    try:
        queryset = queryset.filter(**selector)
    except FieldError as e:
        log.error(f"Wrong keyword for filtering, will return default query! Got FieldError:"
                  f"\n{e}")
    return queryset


class MainPageBlogListView(ListView):
    __url_path = '/blog/'
    # model = Post
    queryset = Post.objects.filter(published__exact=True)
    template_name = 'blog.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(MainPageBlogListView, self).get_context_data(**kwargs)
        context.update(
            selector=blog_selector(self.request.GET),
        )
        return context

    def get_queryset(self):
        selector = blog_selector(self.request.GET)
        # Simple selection:
        if selector.get('tag'):
            self.queryset = Post.objects.filter(tags__name=selector.get('tag'))
        return self.queryset.order_by('-publish_date')


class BlogPost(DetailView):
    __url_path = '/blog/<int:pk>/'
    model = Post
    template_name = 'post.html'
