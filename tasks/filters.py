from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    state_id = filters.NumberFilter(field_name='state__id', lookup_expr='exact')
    state_name = filters.CharFilter(field_name='state__name', lookup_expr='iexact')
    priority_id = filters.NumberFilter(field_name='priority_id', lookup_expr='exact')
    priority_name = filters.CharFilter(field_name='priority__name', lookup_expr='iexact')
    deadline = filters.DateFilter(field_name='deadline', lookup_expr='exact')
    deadline_before = filters.DateFilter(field_name='deadline', lookup_expr='lte')
    deadline_after = filters.DateFilter(field_name='deadline', lookup_expr='gte')

    class Meta:
        model = Task
        fields = ['state_id', 'state_name', 'priority_id', 'priority_name', 'deadline', 'deadline_before', 'deadline_after']