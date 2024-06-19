from django.db import models
from WorkStream.models import Task
from django.conf import settings


class Comment(models.Model):
    
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('customUser', on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField('customUser', related_name='assigned_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

