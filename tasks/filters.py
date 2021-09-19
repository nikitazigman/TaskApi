import logging

from django_filters import FilterSet, ModelChoiceFilter, DateFromToRangeFilter
from .models import Task, List


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TaskFilterSet(FilterSet):
    excluded_list_id = ModelChoiceFilter(
        queryset=List.objects.all(),
        label='excluded_list_id',
        field_name='list_id',
        method='exclude_list_id'
    )
    deadline = DateFromToRangeFilter()

    def exclude_list_id(self, queryset: Task, name, value):
        logger.debug(f'before filtering: {name=}, {value=}')
        queryset = queryset.all().exclude(**{name: value})
        return queryset

    class Meta:
        model = Task
        fields = ['is_active', 'list_id', 'deadline']
        # exclude =
