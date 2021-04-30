import requests
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.contrib.sessions.backends.db import SessionStore

from allauth.socialaccount.models import SocialToken
from rest_framework import viewsets

from .serializers import *
from .models import *

# Create your views here.


class Home(TemplateView):
    template_name = 'home.html'


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = SocialAccount.objects.all()

#deprecated
# This is how you get the OAuth token
# Helper function
# def get_token(request):
#     session = request.session
#     return HttpResponse(session.items())
    # user = request.user
    # result = SocialToken.objects.filter(account__user=user, account__provider="github")
    # print(result.first())
    # return result.first()

# deprecated
# def get_user(request):
#     token = get_token(request)
#     # print(str(token))
#     headers = {'Authorization': 'token ' + str(token)}
#     req = requests.get("https://api.github.com/user", headers=headers)
#     return HttpResponse(req)


# Function to check if a path works
def hello(request):
    return HttpResponse('Hello')

