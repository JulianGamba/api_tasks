from django.contrib import admin
from .models import Task, Priority, State

admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(State)