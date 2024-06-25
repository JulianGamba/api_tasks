from django.contrib import admin

from .models.comment import Comment
from .models.customUser import CustomUser
from .models.priority import Priority
from .models.state import State
from .models.tasks import Task

admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(State)
admin.site.register(CustomUser)
admin.site.register(Comment)
