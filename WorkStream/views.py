from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task, State, Priority, CustomUser, Comment
from .serializers import StateSerializer, PrioritySerializer, CustomUserSerializer, TaskWriteSerializer, TaskReadSerializer, LoginSerializer, CommentSerializer

from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from django.contrib.auth import get_user_model


class StateViewSet(viewsets.ModelViewSet):
    
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def create(self, request, *args, **kwargs):
        # Si los datos enviados son una lista, muchos=True se aplica automáticamente
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class PriorityViewSet(viewsets.ModelViewSet):
    
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def create(self, request, *args, **kwargs):
        # Si los datos enviados son una lista, muchos=True se aplica automáticamente
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()



class CustomUserViewSet(viewsets.ModelViewSet):
    
    queryset =  CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        # Si los datos enviados son una lista, muchos=True se aplica automáticamente
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class RegisterAPIView(generics.CreateAPIView):
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    permission_classes = [AllowAny]

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
        serializer = TaskWriteSerializer(data=request.data, context={'request': request})
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
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_by_owner(request):
    if request.method == 'GET':
        owner_param = request.GET.get('owner')
        
        if owner_param:
            try:
                owner = CustomUser.objects.get(pk=owner_param)
            except (CustomUser.DoesNotExist, ValueError):
                try:
                    owner = CustomUser.objects.get(username=owner_param)
                except CustomUser.DoesNotExist:
                    return Response({'error': 'No hay tarea con ese dueño'}, status=status.HTTP_404_NOT_FOUND)
            
            tasks = Task.objects.filter(owner=owner)
        else:
            tasks = Task.objects.all()
        
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_by_assigned_users(request):
    assigned_users_param = request.GET.get('assigned_users')
    if assigned_users_param:
        try:
            assigned_users = CustomUser.objects.get(Q(pk=assigned_users_param) | Q(username=assigned_users_param))
            tasks = Task.objects.filter(assigned_users=assigned_users)
        except CustomUser.DoesNotExist:
            return Response({'error': 'No hay un usuario asignado'}, status=status.HTTP_404_NOT_FOUND)
    else:
        tasks = Task.objects.all()

    serializer = TaskReadSerializer(tasks, many=True)
    return Response(serializer.data)

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
User = get_user_model()
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.request.data.get('task')
        task = Task.objects.get(id=task_id)
        assigned_users = self.request.data.get('assigned_users', [])
        comment = serializer.save(user=self.request.user, task=task)
        comment.assigned_users.set(assigned_users)
        return comment

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'comment_id'



    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
