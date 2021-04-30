from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.views.generic.base import View
import requests

from .oauth_client import OAuthClient


class GithubOAuthMixin:
    client_id = None
    secret = None
    callback_url = None
    scopes = None

    def get_client_id(self):
        return self.client_id or settings.GITHUB_OAUTH_CLIENT_ID

    def get_secret(self):
        return self.secret or settings.GITHUB_OAUTH_SECRET

    def get_callback_url(self):
        url = self.callback_url or settings.GITHUB_OAUTH_CALLBACK_URL
        return self.request.build_absolute_uri(url)

    def get_scopes(self):
        return self.scopes or getattr(settings, 'GITHUB_OAUTH_SCOPES', [])

    def get_client(self):
        kwargs = {
            'client_id': self.get_client_id(),
            'secret': self.get_secret(),
            'callback_url': self.get_callback_url(),
            'scopes': self.get_scopes()
        }
        return OAuthClient(self.request, **kwargs)


class GithubOAuthLoginView(GithubOAuthMixin, View):

    def get(self, request, *args, **kwargs):
        client = self.get_client()
        return redirect(client.get_redirect_url())


class GithubOAuthCallbackView(GithubOAuthMixin, View):
    backend = None

    def dispatch(self, *args, **kwargs):
        self.token = self.get_token()
        self.data = self.get_data(self.token)
        return super().dispatch(*args, **kwargs)

    def get_backend(self):
        if self.backend:
            return backend
        if hasattr(settings, 'GITHUB_OAUTH_BACKEND'):
            return settings.GITHUB_OAUTH_BACKEND

    def get_user_model(self):
        return get_user_model()

    def get_redirect_url(self):
        return settings.LOGIN_REDIRECT_URL if settings.LOGIN_REDIRECT_URL else '/'

    def get_token(self):
        client = self.get_client()
        return client.get_token(self.request.GET['code'])

    def login(self, user):
        backend = self.get_backend()
        kwargs = {'backend': backend} if backend else {}
        login(self.request, user, **kwargs)

    def get_data(self, token):
        headers = {'Authorization': 'token %s' % token}
        r = requests.get('https://api.github.com/user', headers=headers)
        r.raise_for_status()
        return r.json()

    def redirect(self):
        if 'next' in self.request.GET:
            return redirect(self.request.GET['next'])
        return redirect(self.get_redirect_url())

    def get_user(self, data):
        user_model = self.get_user_model()
        defaults = {user_model.USERNAME_FIELD: data['login']}
        user, _ = user_model.objects.update_or_create(defaults, id=data['id'])
        return user

    def save_token(self, user, token):
        pass

    def get(self, request, *args, **kwargs):
        user = self.get_user(self.data)
        self.login(user)
        self.save_token(user, self.token)
        return self.redirect()
