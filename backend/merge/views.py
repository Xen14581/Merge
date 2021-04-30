import requests
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView

from allauth.socialaccount.models import SocialToken

# from .models import *

# Create your views here.


class Home(TemplateView):
    template_name = 'home.html'


# This is how you get the OAuth token
# Helper function
def get_token(request):
    user = request.user
    result = SocialToken.objects.filter(account__user=user, account__provider="github")
    # print(result.first())
    return result.first()


def get_user(request):
    token = get_token(request)
    # print(str(token))
    headers = {'Authorization': 'token ' + str(token)}
    req = requests.get("https://api.github.com/user", headers=headers)
    return HttpResponse(req)

