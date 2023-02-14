from django_filters.rest_framework import FilterSet, BooleanFilter
from .models import Task


class TaskFilterSet(FilterSet):
    completed = BooleanFilter(
        field_name="completed_at", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = Task
        fields = ["completed", "deadline"]
