from django.test import TestCase
from model_bakery import baker
from task.models import Task
from task.serializers import TaskSerializer


class TaskSerializerTestCase(TestCase):
    def test_user_field_is_exluded(self):
        baker.make("task.Task")
        serializer = TaskSerializer(Task.objects.first())
        self.assertNotIn("user", serializer.data)

    def test_data_fields(self):
        essential_fields = {"title", "level", "deadline", "completed", "days"}

        baker.make("task.Task")
        serializer = TaskSerializer(Task.objects.first())
        data_fields = set(serializer.data)

        self.assertTrue(essential_fields.issubset(data_fields))
