from rest_framework import serializers

from chats.models import RepoChats, Contact
from chats.views import get_user_contact


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class RepoChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoChats
        fields = ('id', 'repo_name', 'messages', 'collaborators')
        read_only = ('id')

    def create(self, validated_data):
        print(validated_data)
        repo_owner = validated_data.pop('repo_owner')
        collaborators = validated_data.pop('collaborators')
        chat = RepoChats()
        chat.save()
        collaborator_list = []
        for collaborator in collaborators:
            username = collaborator['login']
            if str(username) == str(repo_owner):
                collaborator_list.append({str(repo_owner): 'owner'})
            else:
                collaborator_list.append({collaborator['login']: 'collaborator'})
        chat.collaborators = collaborator_list
        chat.repo_owner = repo_owner
        chat.save()
        return chat
