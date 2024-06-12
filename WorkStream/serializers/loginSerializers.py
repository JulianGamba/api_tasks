from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        user = authenticate(username=username, password=password)

        if user:
            return {
                'user': user,
            }
        else:
            raise serializers.ValidationError('Incorrect username or password.')