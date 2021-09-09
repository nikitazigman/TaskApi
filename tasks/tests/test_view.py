from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from tasks.models import Task, List


class TaskViewTest(TestCase):
    def get_user_data(self, username: str, password: str, lists_number: int, tasks_in_list: int, ):
        user = User.objects.create_user(username=username, password=password)
        date = timezone.now()
        for j in range(lists_number):
            list = List.objects.create(
                user_id=user,
                date_created=date
            )
            for i in range(tasks_in_list):
                Task.objects.create(
                    user_id=user,
                    title=f'test task {i} of {user.username}',
                    description=f'test description {i} of {user.username}',
                    comments=f'test comments {i} of {user.username}',
                    deadline=date,
                    list_id=list,
                )
                date += timedelta(1)

    def setUp(self):
        self.password = 'testpassword'
        self.username_one = 'test_one'
        self.username_two = 'test_two'

        self.get_user_data(
            username=self.username_one,
            password=self.password,
            lists_number=4,
            tasks_in_list=10,
        )
        self.get_user_data(
            username=self.username_two,
            password=self.password,
            lists_number=4,
            tasks_in_list=10,
        )

        self.client.login(username=self.username_one, password=self.password)

    def test_get_user_lists(self):
        login = self.client.login(username=self.username_one, password=self.password)
        print(f"{login=}")
        user = User.objects.get(username=self.username_one)
        lists = Task.objects.filter(user_id=user)
        print(f"{user}: {lists}")
        response = self.client.get(reverse('lists'))
        self.assertEqual(response.status_code, 200)

        print(f"{response.json()=}")
        # self.assertTrue(False)

    def test_get_user_detailed_lists(self):
        self.client.login(username=self.username_one, password=self.password)
        self.assertTrue(False)

    def test_get_user_tasks(self):
        self.client.login(username=self.username_one, password=self.password)
        self.assertTrue(False)

    def test_get_user_detailed_task(self):
        self.client.login(username=self.username_one, password=self.password)
        self.assertTrue(False)

    def test_cannot_get_task_of_other_user(self):
        self.client.login(username=self.username_one, password=self.password)
        self.assertTrue(False)

    def test_cannot_get_access_to_data_without_login(self):
        self.client.login(username=self.username_one, password=self.password)
        self.assertTrue(False)
