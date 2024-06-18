from rest_framework import serializers
from WorkStream.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Comment
        fields = ['id', 'task', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
