from django.conf.urls import url
from django.urls import path
from .views import hello

urlpatterns = [
    path('create/', hello, name='create'),
    path('delete/', hello, name='delete'),
]
