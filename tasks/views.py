from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import State, Priority, Task, CustomUser
from .serializers import StateSerializer, PrioritySerializer, TaskReadSerializer, TaskWriteSerializer, LoginSerializer, CustomUserSerializer
from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset =  CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def tasks_detail(request, pk, format=None):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskReadSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskWriteSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_by_state_list(request):
    state_param = request.GET.get('state')
    if state_param:
        try:
            state = State.objects.get(pk=state_param)
        except (State.DoesNotExist, ValueError):
            try:
                state = State.objects.get(name__iexact=state_param)
            except State.DoesNotExist:
                return Response({'error': 'Estado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        tasks = Task.objects.filter(state=state)
    else:
        tasks = Task.objects.all()
    
    serializer = TaskReadSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_by_priority_list(request):
    priority_param = request.GET.get('priority')
    if priority_param:
        try:
            priority = Priority.objects.get(pk=priority_param)
        except(Priority.DoesNotExist, ValueError):
            try:
                priority = Priority.objects.get(name__iexact=priority_param)
            except Priority.DoesNotExist:
                return Response({'error': 'Prioridad no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        tasks = Task.objects.filter(priority=priority)
    else:
        tasks = Task.objects.all()
    
    serializer = TaskReadSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_by_deadline(request):
    deadline_param = request.GET.get('deadline')
    filter_type = request.GET.get('filter', 'exact')
    if deadline_param:
        try:
            if filter_type == 'before':
                tasks = Task.objects.filter(deadline__lt=deadline_param)
            elif filter_type == 'after':
                tasks = Task.objects.filter(deadline__gt=deadline_param)
            else:
                tasks = Task.objects.filter(deadline=deadline_param)

        except ValueError:
            return Response({'error': 'No hay tarea con la fecha proporcionada'}, status=status.HTTP_404_NOT_FOUND)
    else: 
        tasks = Task.objects.all()
        
    serializer = TaskReadSerializer(tasks, many=True)
    return Response(serializer.data)