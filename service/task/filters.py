from day.models import Day
from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Task


class TaskFilterSet(FilterSet):
    completed = filters.BooleanFilter(
        field_name="completed_at", lookup_expr="isnull", exclude=True
    )
    exclude_days = filters.ModelMultipleChoiceFilter(
        queryset=Day.objects.all(), exclude=True, field_name="days"
    )

    class Meta:
        model = Task
        fields = ["completed", "days", "archived", "exclude_days"]
