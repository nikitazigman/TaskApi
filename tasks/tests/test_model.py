from datetime import timedelta

from django.test import TestCase

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from tasks.models import Task, List


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='testpassword')
        date = timezone.now()

        for i in range(10):
            Task.objects.create(
                user_id=user,
                title=f'test task {i}',
                description=f'test description {i}',
                comments=f'test comments {i}',
                deadline=date
            )

            date += timedelta(1)

    def test_title_content(self):
        expected_content = 'test task 0'
        task = Task.objects.first()
        self.assertEqual(task.title, expected_content)

    def test_correct_sort(self):
        tasks = Task.objects.values_list('deadline', flat=True)
        sorted_tasks_list = list(tasks)
        sorted_tasks_list.sort()
        self.assertEqual(list(tasks), sorted_tasks_list)

    def test_cannot_add_wrong_difficulty_value(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(
                user_id=User.objects.first(),
                title=f'test task',
                description=f'test description',
                comments=f'test comments',
                deadline=timezone.now().date() + timedelta(100),
                difficulty=12,
            )