from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    state_id = filters.NumberFilter(field_name='state__id', lookup_expr='exact')
    state_name = filters.CharFilter(field_name='state__name', lookup_expr='iexact')
    priority_id = filters.NumberFilter(field_name='priority__id', lookup_expr='exact')
    priority_name = filters.CharFilter(field_name='priority__name', lookup_expr='iexact')
    deadline = filters.DateFilter(field_name='deadline', lookup_expr='exact')
    deadline_before = filters.DateFilter(field_name='deadline', lookup_expr='lte')
    deadline_after = filters.DateFilter(field_name='deadline', lookup_expr='gte')
    owner_id = filters.NumberFilter(field_name='owner__id', lookup_expr='exact')
    owner_username = filters.CharFilter(field_name='owner__username', lookup_expr='iexact')
    assigned_users_id = filters.NumberFilter(field_name='assigned_users__id', lookup_expr='exact')
    assigned_users_username = filters.CharFilter(field_name='assigned_users__username', lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['state_id', 'state_name', 'priority_id', 'priority_name', 'deadline', 'deadline_before', 'deadline_after', 'owner_id', 'owner_username', 'assigned_users_id', 'assigned_users_username']