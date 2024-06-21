from django.contrib.auth import get_user_model
from rest_framework import serializers

from WorkStream.models import Comment, Task

CustomUser = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ["id", "user", "task", "text", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
