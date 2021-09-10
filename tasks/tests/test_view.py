from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from tasks.models import Task, List
from tasks.serializers import TaskSerializer, ListSerializer


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
        self.list_number = 4
        self.task_number_in_one_list = 10

        self.get_user_data(
            username=self.username_one,
            password=self.password,
            lists_number=self.list_number,
            tasks_in_list=self.task_number_in_one_list,
        )
        self.get_user_data(
            username=self.username_two,
            password=self.password,
            lists_number=self.list_number,
            tasks_in_list=self.task_number_in_one_list,
        )

    def test_get_user_lists(self):
        self.assertTrue(self.client.login(username=self.username_one, password=self.password))
        response = self.client.get(reverse('lists'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.list_number)

        user = User.objects.get(username=self.username_one)
        lists = List.objects.filter(user_id=user)

        for list_obj, resp_obj in zip(lists, response.json()):
            serialized_list_obj = ListSerializer(list_obj)
            self.assertEqual(serialized_list_obj.data, resp_obj)

    def test_get_user_detailed_lists(self):
        list_id = 2

        self.assertTrue(self.client.login(username=self.username_one, password=self.password))
        response = self.client.get(reverse('detailed-list', kwargs={'pk': list_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.task_number_in_one_list)

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user, list_id=list_id)

        for task_obj, resp_obj in zip(tasks, response.json()):
            serialized_task_obj = TaskSerializer(task_obj)
            self.assertEqual(serialized_task_obj.data, resp_obj)

    def test_get_user_tasks(self):
        self.assertTrue(self.client.login(username=self.username_one, password=self.password))
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.task_number_in_one_list * self.list_number)

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user)

        for task_obj, resp_obj in zip(tasks, response.json()):
            serialized_task_obj = TaskSerializer(task_obj)
            self.assertEqual(serialized_task_obj.data, resp_obj)

    def test_get_user_detailed_task(self):
        task_id = 2

        self.assertTrue(self.client.login(username=self.username_one, password=self.password))
        response = self.client.get(reverse('detailed-task', kwargs={'pk': task_id}))
        self.assertEqual(response.status_code, 200)

        task = Task.objects.get(id=task_id)
        serialized_task = TaskSerializer(task)
        self.assertEqual(serialized_task.data, response.json())

    def test_cannot_get_task_of_other_user(self):
        self.assertTrue(self.client.login(username=self.username_one, password=self.password))

        user = User.objects.get(username=self.username_two)
        user_two_task = Task.objects.filter(user_id=user).first()
        task_id = user_two_task.id

        response = self.client.get(reverse('detailed-task', kwargs={'pk': task_id}))

        self.assertEqual(response.status_code, 404)

    def test_cannot_get_access_to_data_without_login(self):
        response = self.client.get(reverse('detailed-task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('detailed-list', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('lists'))
        self.assertEqual(response.status_code, 403)
