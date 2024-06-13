from rest_framework import serializers
from WorkStream.models import State, Priority, Comment, CustomUser, Task
from .stateSerializers import StateSerializer
from .prioritySerializers import PrioritySerializer
from .customUserSerializers import CustomUserSerializer
from .commentSerializers import CommentSerializer

class TaskReadSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    priority = PrioritySerializer()
    owner = CustomUserSerializer()
    assigned_users = CustomUserSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)  # Read-only comments

    class Meta:
        model = Task
        fields = '__all__'

# Serializador para la escritura
class TaskWriteSerializer(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    comments = CommentSerializer(many=True, required=False)  # Handle multiple comments


    class Meta:
        model = Task
        exclude = ['owner']

    def create(self, validated_data):
        user = self.context['request'].user
        comments_data = validated_data.pop('comments', [])
        assigned_users_data = validated_data.pop('assigned_users', [])
        validated_data['owner'] = user
        task = Task.objects.create(**validated_data)
        
        if assigned_users_data:
            task.assigned_users.set(assigned_users_data)
        
        for comment_data in comments_data:
            Comment.objects.create(task=task, user=user, **comment_data)
        
        return task

    def update(self, instance, validated_data):
        comments_data = validated_data.pop('comments', [])
        instance = super().update(instance, validated_data)
        for comment_data in comments_data:
            Comment.objects.create(task=instance, user=self.context['request'].user, **comment_data)
        return instance