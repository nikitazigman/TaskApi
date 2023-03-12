from django.core.management import call_command
from django.test import TestCase
from task.filters import TaskFilterSet
from task.models import Task


class TaskFilterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        call_command("generate_test_data")

    def test_filter_completed(self) -> None:
        tasks = Task.objects.all()
        task_filter = TaskFilterSet(data={"completed": False}, queryset=tasks)
        self.assertEqual(
            list(task_filter.qs), list(Task.objects.filter(completed_at=None))
        )

    def test_filter_deadline(self) -> None:
        tasks = Task.objects.all()
        task_filter = TaskFilterSet(data={"completed": True}, queryset=tasks)
        self.assertEqual(
            list(task_filter.qs), list(Task.objects.exclude(completed_at=None))
        )

    def test_filter_single_day(self) -> None:
        tasks = Task.objects.all()

        test_day = tasks.exclude(days=None).first().days.first()

        task_filter = TaskFilterSet(data={"days": [test_day]}, queryset=tasks)
        self.assertEqual(list(task_filter.qs), list(Task.objects.filter(days=test_day)))

    def test_filter_archived(self) -> None:
        tasks = Task.objects.all()
        task_filter = TaskFilterSet(data={"archived": True}, queryset=tasks)
        self.assertEqual(list(task_filter.qs), list(Task.objects.filter(archived=True)))
