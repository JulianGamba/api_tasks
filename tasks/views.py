from rest_framework import viewsets
from .models import State, Priority, Task
from .serializers import StateSerializer, PrioritySerializer, TaskReadSerializer, UserSerializer, TaskWriteSerializer
from .filters import TaskFilter
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    filterset_class = TaskFilter
 
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskReadSerializer
        return TaskWriteSerializer