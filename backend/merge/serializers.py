from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import Todo, MergeProfile


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'completed', 'repo', 'assigned_merge_user', 'deadline')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    merge_password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = MergeProfile
        fields = ('id', 'user', 'merge_username', 'merge_password')

    def create(self, validated_data):
        validated_data['merge_password'] = make_password(validated_data.get('merge_password'))
        return super(ProfileSerializer, self).create(validated_data)
