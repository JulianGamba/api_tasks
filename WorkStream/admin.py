from django.contrib import admin
from .models.state import State
from .models.customUser import CustomUser
from .models.tasks import Task
from .models.priority import Priority


admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(State)
admin.site.register(CustomUser)
