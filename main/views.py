import json
import logging
import ast

from django.db.models import Count, Q
from django.views.generic import TemplateView, ListView
from django.contrib.redirects.models import Redirect

from blog.models import Post, Tag
from main.models import NetworkVisitorsAddresses, URLPathsVisitors, Options

log = logging.getLogger("core")


def is_json(item):
    try:
        json.load(item)
    except json.decoder.JSONDecodeError:
        return False
    return True


def evaluate_option(value):
    return ast.literal_eval(value)


def main_selector(request_GET):
    """
    :param request_GET:  self.request.GET
    :return: dict of evaluated query values
    """
    selector = dict(
        tag=request_GET.get('tag', None),
    )
    validated = {key: value for key, value in selector.items() if value and value is not None}
    return validated


def load_option(key='hide.url_path'):
    option = Options.objects.get(option_key__exact=key)
    option_value = None

    # Use this option, or not:
    if option.option_bool:
        option_value = option.option_value
        # This is a list:
        if '[' in option_value and ']' in option_value:
            option_value = evaluate_option(option_value)
        # This is set of JSON/Dict?
        if '{' in option_value and '}' in option_value:
            # As JSON
            if is_json(option_value):
                option_value = json.loads(option_value)
            # As set
            else:
                option_value = evaluate_option(option_value)

    return option.option_bool, option_value


class MainPage(TemplateView):
    template_name = 'main/main_body.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context.update(
            debug=False,
            # objects=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        main_data = dict(
            posts=Post.objects.filter(published=True),
            tags=Tag.objects.all(),
        )
        return main_data


class FeedBackComments(TemplateView):
    template_name = 'main/feedback.html'


class RobotsTxt(TemplateView):
    template_name = 'main/robots.html'


class Visitors(ListView):
    model = NetworkVisitorsAddresses
    queryset = NetworkVisitorsAddresses.objects.all().order_by('-updated_at')
    template_name = 'visitors.html'
    title = "Network visitor addresses"
    paginate_by = 100
    limit_to = 30


    def get_context_data(self, **kwargs):
        context = super(Visitors, self).get_context_data(**kwargs)
        context.update(
            selector=main_selector(self.request.GET),
            title=self.title,
            limit_to=self.limit_to
        )
        return context

    def get_queryset(self):
        selector = main_selector(self.request.GET)
        # Simple selection:
        if selector.get('tag'):
            self.queryset = self.queryset.filter(tags__name=selector.get('tag'))

        return self.queryset.order_by('-updated_at')


class VisitorsUrls(ListView):
    model = URLPathsVisitors
    queryset = URLPathsVisitors.objects.all().order_by('-created_at')
    template_name = 'visitors_urls.html'
    title = "Visitor URL hits"
    paginate_by = 100
    limit_to = 30

    def get_context_data(self, **kwargs):
        context = super(VisitorsUrls, self).get_context_data(**kwargs)
        context.update(
            selector=main_selector(self.request.GET),
            title=self.title,
            limit_to=self.limit_to
        )
        return context

    def get_queryset(self):
        selector = main_selector(self.request.GET)
        # Simple selection:
        if selector.get('tag'):
            self.queryset = self.queryset.filter(tags__name=selector.get('tag'))

        to_skip, skipable_urls = load_option(key='hide.url_path')

        # Get all redirects where my url_path is found
        redirects = Redirect.objects.all()
        # Exclude urls which are mentioned in redirects.
        self.queryset = self.queryset.filter(
            ~Q(url_path__in=redirects.values_list('old_path', flat=True)) &
            ~Q(url_path__in=redirects.values_list('new_path', flat=True))
        )

        if to_skip and skipable_urls is not None:
            self.queryset = self.queryset.filter(~Q(url_path__in=skipable_urls))

        # For now only show URLs with max hists:
        self.queryset = self.queryset.all().annotate(total=Count('visitor_rel_url_path')).order_by('-total')
        self.queryset = self.queryset.filter(total__gte=self.limit_to)

        return self.queryset
