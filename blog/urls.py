from django.urls import path

from blog.views import *

urlpatterns = [
    # Home
    path('', MainPageBlogListView.as_view(), name='blog'),
    # path('blog/', MainPageBlogListView.as_view(), name='blog'),
]
