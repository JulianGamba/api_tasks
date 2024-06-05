from rest_framework import serializers
from .models import Task, Priority, State, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'full_name', 'avatar', 'birth_date', 'identification')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            full_name=validated_data.get('full_name', ''),
            avatar=validated_data.get('avatar', None),
            birth_date=validated_data.get('birth_date', None),
            identification=validated_data.get('identification', None),
        )
        return user

class TaskReadSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    priority = PrioritySerializer()
    owner = CustomUserSerializer()
    assigned_users = CustomUserSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'

# Serializador para la escritura
class TaskWriteSerializer(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Task
        exclude = ['owner']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data