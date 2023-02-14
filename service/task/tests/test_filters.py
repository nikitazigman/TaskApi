from django.test import TestCase
from model_bakery import baker
from task.filters import TaskFilterSet
from task.models import Task


class TaskFilterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        baker.make("task.Task", _quantity=20)

    def test_filter_completed(self) -> None:
        tasks = Task.objects.all()
        filter = TaskFilterSet(data={"completed": False}, queryset=tasks)
        self.assertEqual(list(filter.qs), list(Task.objects.filter(completed_at=None)))

    def test_filter_deadline(self) -> None:
        tasks = Task.objects.all()
        filter = TaskFilterSet(data={"completed": True}, queryset=tasks)
        self.assertEqual(list(filter.qs), list(Task.objects.exclude(completed_at=None)))
