from allauth.socialaccount.models import SocialAccount
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('id', 'user_id', 'provider', 'uid', 'last_login', 'date_joined', 'extra_data')
