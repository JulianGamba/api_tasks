from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import task_list_create, tasks_detail, task_by_state_list, task_by_priority_list, task_by_deadline
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'states', views.StateViewSet, basename='state')
router.register(r'prioritys', views.PriorityViewSet, basename='priority')
router.register(r'users', views.UserViewSet, basename='user')
# router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', task_list_create, name='task-list-create'),
    path('tasks/<int:pk>/', tasks_detail, name='task-detail'),
    path('tasks/by_state/', task_by_state_list, name='task-by-state-list'),
    path('tasks/by_priority/', task_by_priority_list, name='task-by-priority-list'),
    path('tasks/by_deadline/', task_by_deadline, name='task-by-deadline-list'),
]


#     path('user/tasks/', user_task_list, name='user-task-list'),