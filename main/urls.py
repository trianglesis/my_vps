from django.urls import path

from main.views import *

urlpatterns = [
    # Home
    path('', MainPage.as_view(), name='home'),
    path('feedback/', FeedBackComments.as_view(), name='feedback'),
    path('visitors/', Visitors.as_view(), name='visitors'),
    path('visitors_urls/', VisitorsUrls.as_view(), name='visitors_urls'),
    path('visitors_gets/', VisitorsGets.as_view(), name='visitors_gets'),
    path('visitors_posts/', VisitorsPosts.as_view(), name='visitors_posts'),
]
