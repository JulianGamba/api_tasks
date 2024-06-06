from django.contrib import admin
from .models import Task, Priority, State
from .models.customUser import CustomUser


admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(State)
admin.site.register(CustomUser)
