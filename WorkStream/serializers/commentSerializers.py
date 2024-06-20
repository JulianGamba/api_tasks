from rest_framework import serializers
from WorkStream.models import Comment, Task, customUser
user = customUser.objects.all()


class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=customUser.objects.all(), default=serializers.CurrentUserDefault())
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=customUser.objects.all(), required=False)


    class Meta:
        model = Comment
        fields = ['id' , 'user', 'task', 'assigned_users', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users', [])
        comment = Comment.objects.create(**validated_data)
        comment.assigned_users.set(assigned_users)
        return comment

    def update(self, instance, validated_data):
        assigned_users = validated_data.pop('assigned_users', [])
        instance = super().update(instance, validated_data)
        instance.assigned_users.set(assigned_users)
        return instance
