import logging

from django.db.models import QuerySet
from django_filters import DateFromToRangeFilter, FilterSet, ModelChoiceFilter

from .models import Task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class UserFilterSet(FilterSet):
    def filter_queryset(self, queryset):
        queryset = queryset.filter(user_id=self.request.user.id)
        return super(UserFilterSet, self).filter_queryset(queryset)


class TaskFilterSet(UserFilterSet):
    excluded_day = ModelChoiceFilter(
        queryset=Day.objects.all(),
        label="excluded_day",
        field_name="day",
        method="exclude_day",
    )
    deadline = DateFromToRangeFilter()

    def exclude_day(self, queryset: QuerySet[Task], name, value):
        logger.debug(f"got filtering args: {name=}, {value=}")

        queryset = queryset.all().exclude(**{name: value})
        return queryset

    class Meta:
        model = Task
        fields = ["completed", "date", "deadline"]
