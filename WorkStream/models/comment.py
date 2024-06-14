from django.db import models
from django.contrib.auth import get_user_model
from WorkStream.models import Task  

User = get_user_model()

class Comment(models.Model):
    Task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    User = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]
