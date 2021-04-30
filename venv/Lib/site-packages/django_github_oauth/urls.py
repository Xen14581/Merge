from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import GithubOAuthCallbackView, GithubOAuthLoginView

app_name = 'github_oauth'

urlpatterns = [
    path('callback', GithubOAuthCallbackView.as_view(),name='callback'),
    path('login', GithubOAuthLoginView.as_view(),name='login'),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL if settings.LOGOUT_REDIRECT_URL else '/'),name='logout'),
]
