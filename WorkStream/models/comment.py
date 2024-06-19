from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from WorkStream.models import Task

User = get_user_model()


class Comment(models.Model):
    task = models.ForeignKey('Task', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField(User, related_name='assigned_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
