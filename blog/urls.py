from django.urls import path

from blog.views import *

urlpatterns = [
    # Home
    path('', MainPageBlogListView.as_view(), name='blog'),
    path('post/<slug:slug>/', BlogPost.as_view(), name='post'),
    path('post_id/<int:pk>/', BlogPost.as_view(), name='post_id'),

]
