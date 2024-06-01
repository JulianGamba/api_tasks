from rest_framework import viewsets
from .models import State, Priority, Task, CustomUser
from .serializers import StateSerializer, PrioritySerializer, TaskSerializer, UserSerializer
from django.contrib.auth.models import User


from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CustomUserSerializer


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
    serializer_class = TaskSerializer
    
 
class CustomUserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
