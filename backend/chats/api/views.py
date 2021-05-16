from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from chats.models import RepoChats, Contact
from chats.views import get_user_contact
from .serializers import RepoChatSerializer

User = get_user_model()


class ChatListView(ListAPIView):
    serializer_class = RepoChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = RepoChats.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset


class ChatDetailView(RetrieveAPIView):
    queryset = RepoChats.objects.all()
    serializer_class = RepoChatSerializer
    # permission_classes = (permissions.AllowAny, )


class ChatCreateView(CreateAPIView):
    queryset = RepoChats.objects.all()
    serializer_class = RepoChatSerializer
    # permission_classes = (permissions.IsAuthenticated, )


class ChatUpdateView(UpdateAPIView):
    queryset = RepoChats.objects.all()
    serializer_class = RepoChatSerializer
    # permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = RepoChats.objects.all()
    serializer_class = RepoChatSerializer
    # permission_classes = (permissions.IsAuthenticated, )
