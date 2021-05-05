from django.conf.urls import url
from django.urls import path
from .views import hello, get_user_repos

urlpatterns = [
    path('create/', hello, name='create'),
    path('delete/', hello, name='delete'),
    path('view/', get_user_repos, name='view'),
]
