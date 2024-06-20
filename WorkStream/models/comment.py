from django.contrib.auth import get_user_model
from django.db import models
from WorkStream.models import Task
from WorkStream.models import CustomUser

CustomUser = get_user_model()

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments_created')
    text = models.TextField()
    assigned_users = models.ManyToManyField(CustomUser, related_name='assigned_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
