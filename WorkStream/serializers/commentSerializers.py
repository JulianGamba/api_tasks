from rest_framework import serializers
from WorkStream.models import Comment, Task, CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'assigned_users', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users', [])
        comment = Comment.objects.create(**validated_data)
        comment.assigned_users.set(assigned_users)
        return comment

    def update(self, instance, validated_data):
        assigned_users = validated_data.pop('assigned_users', [])
        comment = super().update(instance, validated_data)
        comment.assigned_users.set(assigned_users)
        return comment
