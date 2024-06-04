from rest_framework import viewsets
from .models import State, Priority, Task
from .serializers import StateSerializer, PrioritySerializer, TaskReadSerializer, UserSerializer, TaskWriteSerializer
from .filters import TaskFilter
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedOrReadOnly

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    filterset_class = TaskFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskReadSerializer
        return TaskWriteSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)