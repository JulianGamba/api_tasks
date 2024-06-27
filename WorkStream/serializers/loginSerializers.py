from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        print(password, username)
        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        user = authenticate(username=username, password=password)
        print(user)

        if user:
            return {
                "user": user,
            }
        else:
            raise serializers.ValidationError("Incorrect username or password.")
