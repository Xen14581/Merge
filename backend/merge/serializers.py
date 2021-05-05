import collections
import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict

from rest_framework import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Todo, MergeProfile


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'completed', 'repo', 'assigned_merge_user', 'deadline')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile')
        # fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    merge_password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = MergeProfile
        fields = ('id', 'user', 'merge_username', 'merge_password')

    def create(self, validated_data):
        print(validated_data['merge_password'])
        validated_data['merge_password'] = make_password(validated_data.get('merge_password'))
        print(validated_data['merge_password'])
        return super(ProfileSerializer, self).create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass
        else:
            request_data = json.loads(json.dumps(request.data))
            # print(request_data)
            merge_username = request_data.get("username")
            merge_password = request_data.get("password")
            profile_has_expired = False
            try:
                profile = User.objects.get(
                    profile__merge_username=merge_username
                )
            except User.DoesNotExist:
                profile_has_expired = True
            finally:
                if profile_has_expired:
                    error_message = "This profile not found"
                    error_name = "missing_profile"
                    raise exceptions.AuthenticationFailed(error_message, error_name)
        finally:
            request = self.context["request"]
            request_data = json.loads(json.dumps(request.data))
            profile = User.objects.get(
                profile__merge_username=request_data.get("username")
            )
            custom_attrs = dict(attrs)
            custom_attrs['username'] = profile
            attrs = collections.OrderedDict(custom_attrs)
            data = super().validate(attrs)
            data['user'] = model_to_dict(profile)
            return data
