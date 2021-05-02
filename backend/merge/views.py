import requests
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import TemplateView
# from django.contrib.sessions.backends.db import SessionStore

from allauth.socialaccount.models import SocialToken, SocialAccount
from rest_framework import viewsets, status
from rest_framework.response import Response

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
    queryset = User.objects.all()


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = MergeProfile.objects.all()

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# deprecated
# This is how you get the OAuth token
# Helper function
def get_token(request):
    user = request.user
    print(request.data)
    result = SocialToken.objects.filter(account__user=user, account__provider="github")
    return result.first()

# deprecated
def get_user(request):
    # token = get_token(request)
    # # print(str(token))
    # headers = {'Authorization': 'token ' + str(token)}
    # req = requests.get("https://api.github.com/user", headers=headers)
    # # print(json.loads(req.text))
    # return HttpResponse(json.dumps(json.loads(req.text)))
    users = SocialAccount.objects.values_list("extra_data")
    return JsonResponse(users.first()[0], safe=False)

# Function to check if a path works
def hello(request):
    return HttpResponse('Hello')


def repos(request, username):
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    return JsonResponse(response.json()[:], safe=False)
