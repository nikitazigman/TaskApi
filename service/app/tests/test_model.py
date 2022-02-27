from datetime import timedelta

from app.models import Day, Task
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="test", password="testpassword")
        date = timezone.now()

        for i in range(10):
            Task.objects.create(
                user_id=user.id,
                title=f"test task {i}",
                description=f"test description {i}",
                comments=f"test comments {i}",
                deadline=date,
            )

            date += timedelta(1)

    def test_title_content(self):
        expected_content = "test task 0"
        task = Task.objects.first()
        self.assertEqual(task.title, expected_content)

    def test_correct_sort(self):
        tasks = Task.objects.values_list("deadline", flat=True)
        sorted_tasks_list = list(tasks)
        sorted_tasks_list.sort()
        self.assertEqual(list(tasks), sorted_tasks_list)

    def test_cannot_add_wrong_difficulty_value(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(
                user_id=User.objects.first().id,
                title="test task",
                description="test description",
                comments="test comments",
                deadline=timezone.now().date() + timedelta(100),
                difficulty=12,
            )


class ListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="testpassword")
        date = timezone.now()

        for i in range(10):
            Day.objects.create(user_id=self.user.id, date_created=date)
            date += timedelta(1)

    def test_correct_sort(self):
        lists = Day.objects.values_list("date_created", flat=True)
        sorted_lists = list(lists)
        sorted_lists.sort(reverse=True)
        self.assertEqual(list(lists), sorted_lists)

    def test_unique_user_id_and_date_created(self):
        with self.assertRaises(IntegrityError):
            Day.objects.create(user_id=self.user.id, date_created=timezone.now())
