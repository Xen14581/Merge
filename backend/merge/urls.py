from django.conf.urls import url
from django.urls import path
from .views import get_user_repos, create_repo, delete_repo

urlpatterns = [
    path('create/', create_repo, name='create'),
    path('delete/', delete_repo, name='delete'),
    path('view/', get_user_repos, name='view'),
]
