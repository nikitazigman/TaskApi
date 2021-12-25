import logging

from django.db.models import QuerySet
from django_filters import DateFromToRangeFilter, FilterSet, ModelChoiceFilter

from .models import List, Task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class UserFilterSet(FilterSet):
    def filter_queryset(self, queryset):
        queryset = queryset.filter(user_id=self.request.user)
        return super(UserFilterSet, self).filter_queryset(queryset)


class TaskFilterSet(UserFilterSet):
    excluded_list_id = ModelChoiceFilter(
        queryset=List.objects.all(),
        label="excluded_list_id",
        field_name="list_id",
        method="exclude_list_id",
    )
    deadline = DateFromToRangeFilter()

    def exclude_list_id(self, queryset: QuerySet[Task], name, value):
        logger.debug(f"got filtering args: {name=}, {value=}")
        queryset = queryset.all().exclude(**{name: value})
        return queryset

    class Meta:
        model = Task
        fields = ["is_active", "list_id", "deadline"]
        # exclude =
