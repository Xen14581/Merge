from django.conf import settings
from django.utils.http import urlencode
import requests


class OAuthClient(object):
    client_id = None
    secret = None
    callback_url = None
    scopes = None

    def __init__(self, request, **kwargs):
        self.request = request
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_client_id(self):
        return self.client_id or settings.GITHUB_OAUTH_CLIENT_ID

    def get_secret(self):
        return self.secret or settings.GITHUB_OAUTH_SECRET

    def get_callback_url(self):
        url = self.callback_url or settings.GITHUB_OAUTH_CALLBACK_URL
        return self.request.build_absolute_uri(url)

    def get_scopes(self):
        return self.scopes or getattr(settings, 'GITHUB_OAUTH_SCOPES', [])

    def get_redirect_url(self):
        scopes = self.get_scopes()
        return 'https://github.com/login/oauth/authorize?%s' % urlencode({
            'client_id': self.get_client_id(),
            'redirect_uri': self.get_callback_url(),
            'scope': ' '.join(set(scopes if scopes else [])),
            'response_type': 'code'
        })

    def get_token(self, code):
        data = {
            'code': code,
            'client_id': self.get_client_id(),
            'client_secret': self.get_secret(),
            'grant_type': 'authorization_code',
            'redirect_uri': self.get_callback_url()
        }
        r = requests.post(
            'https://github.com/login/oauth/access_token', data=data)
        r.raise_for_status()
        for s in filter(lambda s: 'access_token' in s, r.text.split('&')):
            return s.split('=')[1]
