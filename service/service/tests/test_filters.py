from django.core.management import call_command
from django.http import HttpRequest
from django.test import TestCase
from task.models import Task

from service.filters import BelongToOwnerFilter


class FilterBackendTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        call_command("generate_test_data")

    def test_objects_belong_to_owner(self) -> None:
        test_queryset = Task.objects.all()
        test_user = test_queryset[0].user
        fake_request = HttpRequest()
        fake_request.user = test_user

        backend_filter = BelongToOwnerFilter()

        filtered_queryset = backend_filter.filter_queryset(
            request=fake_request, queryset=test_queryset, view=None
        )
        expected_queryset = Task.objects.filter(user=test_user).all()

        self.assertEqual(list(filtered_queryset), list(expected_queryset))
