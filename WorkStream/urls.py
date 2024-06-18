from django.urls import path
from WorkStream.views import *
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Trello Api",
      default_version='v1',
      description="Api simulando el funcionamiento del trello",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

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
    path('tasks/by_owner/', task_by_owner, name='task-by-owner-list'),
    path('tasks/by_assigned_users/', task_by_assigned_users, name='task-by-assigned-users-list'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]