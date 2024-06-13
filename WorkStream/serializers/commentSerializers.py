from rest_framework import serializers
from WorkStream.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Solo lectura, se establece automáticamente

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']
