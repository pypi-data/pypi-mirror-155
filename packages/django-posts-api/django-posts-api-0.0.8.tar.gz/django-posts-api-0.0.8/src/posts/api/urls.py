from django.urls import path

from .views import api_posts_lists

app_name = "posts"
urlpatterns = [
    path("", api_posts_lists, name='posts-list'),
]
