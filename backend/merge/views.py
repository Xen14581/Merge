import requests
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView

from allauth.socialaccount.models import SocialToken, SocialAccount
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from .models import *
from chats.models import RepoChats

'''Class Based Views Section'''


class Home(TemplateView):
    template_name = 'home.html'


class TodoView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def put(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
    queryset = MergeProfile.objects.all()

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


'''Helper Functions'''


# Function to check if a path works
def hello(request):
    return HttpResponse('Hello')


# This is how you get the OAuth token
def get_oauthtoken(request):
    username = request.data['username']
    user = User.objects.get(username=username)
    result = SocialToken.objects.filter(account__user=user, account__provider="github")
    return result.first()


# Using Github API v4 to get data
def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


'''Function Based Views Section'''


@api_view(['POST', ])
def get_user(request):
    token = get_oauthtoken(request)
    headers = {'Authorization': 'token ' + str(token)}
    req = requests.get("https://api.github.com/user", headers=headers)
    return Response(json.dumps(json.loads(req.text)))


@api_view(['POST', ])
def get_user_repos(request):
    token = get_oauthtoken(request)
    headers = {'Authorization': 'token ' + str(token)}
    query = '''
    {
        viewer {
        repositories(first: 100, affiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER],
                        ownerAffiliations:[OWNER, ORGANIZATION_MEMBER, COLLABORATOR]) {
          totalCount
          nodes{
            name
              owner {
                login
              }
               collaborators {
               nodes {
                 login
               }
              }
            }
          }
       }
    }
    '''
    req = run_query(query=query, headers=headers)
    return Response(json.dumps(req))


@api_view(['POST', ])
def create_repo(request):
    token = get_oauthtoken(request)
    repo_name = request.data['repo_name']
    headers = {'Authorization': 'token ' + str(token)}
    data = {"name": repo_name}
    req = requests.post("https://api.github.com/user/repos", headers=headers, data=json.dumps(data))
    collaborators = [{request.data['username']: 'owner'}]
    chat = RepoChats()
    chat.repo_name = repo_name
    chat.collaborators = collaborators
    chat.save()
    return Response(json.dumps(json.loads(req.text)))


@api_view(['POST', ])
def delete_repo(request):
    token = get_oauthtoken(request)
    username = request.data['username']
    repo_name = request.data['repo_name']
    headers = {'Authorization': 'token ' + str(token)}
    req = requests.delete(f"https://api.github.com/repos/{username}/{repo_name}", headers=headers)
    return Response(req)
