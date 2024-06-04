from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'states', views.StateViewSet, basename='state')
router.register(r'prioritys', views.PriorityViewSet, basename='priority')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'tasks', views.TaskViewSet, basename='task')


urlpatterns = [
    path('', include(router.urls)),
]