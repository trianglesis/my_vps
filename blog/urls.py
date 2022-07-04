from django.urls import path

from blog.views import *

urlpatterns = [
    # Home
    path('', MainPageBlog.as_view(), name='blog'),
    # path('blog/', MainPageBlog.as_view(), name='blog'),
]
