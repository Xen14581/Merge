from django.conf.urls import url
from django.urls import path
from .views import hello, repos

urlpatterns = [
    path('create/', hello, name='create'),
    path('delete/', hello, name='delete'),
    path('view/<str:username>', repos, name='view')
]
