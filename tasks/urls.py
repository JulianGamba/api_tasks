from django.urls import path, include
from tasks.views import *
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('states/', StateViewSet.as_view({'get': 'list', 'post': 'create'}), name='state-list'),
    path('states/<int:pk>/', StateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='state-detail'),
    path('priorities/', PriorityViewSet.as_view({'get': 'list', 'post': 'create'}), name='priority-list'),
    path('priorities/<int:pk>/', PriorityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='priority-detail'),
    path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='customuser-list'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='customuser-detail'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('tasks/', task_list_create, name='task-list-create'),
    path('tasks/<int:pk>/', tasks_detail, name='task-detail'),
    path('tasks/by_state/', task_by_state_list, name='task-by-state-list'),
    path('tasks/by_priority/', task_by_priority_list, name='task-by-priority-list'),
    path('tasks/by_deadline/', task_by_deadline, name='task-by-deadline-list'),
]