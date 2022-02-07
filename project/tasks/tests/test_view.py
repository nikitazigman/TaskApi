import logging
from datetime import timedelta
from typing import Union

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from tasks.models import List, Task
from tasks.serializers import ListSerializer, TaskSerializer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskViewTest(TestCase):
    def get_user_data(
        self,
        username: str,
        password: str,
        lists_number: int,
        tasks_in_list: int,
    ):
        user = User.objects.create_user(username=username, password=password)
        date = timezone.now()
        for j in range(lists_number):
            list = List.objects.create(user_id=user, date_created=date)
            for i in range(tasks_in_list):
                Task.objects.create(
                    user_id=user,
                    title=self.fake.text(max_nb_chars=20),
                    description=self.fake.text(max_nb_chars=100),
                    comments=self.fake.text(max_nb_chars=100),
                    deadline=self.fake.date_between(start_date="-1y", end_date="+1y"),
                    list_id=list,
                )
                date += timedelta(1)

    def setUp(self):
        self.fake = Faker()

        self.password = self.fake.password()
        self.username_one = self.fake.name()
        self.username_two = self.fake.name()

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

        self.assertTrue(
            self.client.login(username=self.username_one, password=self.password)
        )

    def compare_response_with_queryset(
        self, response_json: dict, queryset: Union[List, Task]
    ):
        serializer_type = {
            "Task": TaskSerializer,
            "List": ListSerializer,
        }

        serializer = serializer_type[type(queryset.first()).__name__]

        for query_obj, resp_obj in zip(queryset, response_json):
            serialized_obj = serializer(query_obj)
            logger.debug(f"{serialized_obj.data['id']=} == {resp_obj['id']=}")
            self.assertEqual(serialized_obj.data, resp_obj)

    def test_get_user_lists(self):
        response = self.client.get(reverse("lists"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.list_number)

        user = User.objects.get(username=self.username_one)
        lists = List.objects.filter(user_id=user)

        self.compare_response_with_queryset(
            response_json=response.json(), queryset=lists
        )

    def test_get_user_detailed_lists(self):
        user = User.objects.get(username=self.username_one)
        lists = List.objects.filter(user_id=user)
        list_id = lists[2].id

        response = self.client.get(reverse("tasks"), {"list_id": list_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.task_number_in_one_list)

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user, list_id=list_id)

        self.compare_response_with_queryset(
            response_json=response.json(), queryset=tasks
        )

    def test_get_user_tasks(self):
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()), self.task_number_in_one_list * self.list_number
        )

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user)

        self.compare_response_with_queryset(
            response_json=response.json(), queryset=tasks
        )

    def test_get_user_active_tasks(self):
        response = self.client.get(reverse("tasks"), {"is_active": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()), self.task_number_in_one_list * self.list_number
        )

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user, is_active=True)

        self.compare_response_with_queryset(
            response_json=response.json(), queryset=tasks
        )

    def test_get_user_active_tasks_for_the_list(self):
        user = User.objects.get(username=self.username_one)
        lists = List.objects.filter(user_id=user)
        list_id = lists[2].id

        deadline_after = timezone.now().date() + timedelta(days=2)

        response = self.client.get(
            reverse("tasks"),
            {
                "is_active": True,
                "excluded_list_id": list_id,
                "deadline_after": str(deadline_after),
            },
        )

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(
            user_id=user, is_active=True, deadline__gte=deadline_after
        ).exclude(list_id=list_id)

        self.compare_response_with_queryset(
            response_json=response.json(), queryset=tasks
        )

    def test_get_user_detailed_task(self):
        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user)
        task_id = tasks[2].id

        response = self.client.get(reverse("detailed-task", kwargs={"pk": task_id}))
        self.assertEqual(response.status_code, 200)

        task = Task.objects.get(id=task_id)
        serialized_task = TaskSerializer(task)
        self.assertEqual(serialized_task.data, response.json())

    def test_cannot_get_task_of_other_user(self):

        user = User.objects.get(username=self.username_two)
        user_two_task = Task.objects.filter(user_id=user).first()
        task_id = user_two_task.id

        response = self.client.get(reverse("detailed-task", kwargs={"pk": task_id}))

        self.assertEqual(response.status_code, 404)

    def test_cannot_get_access_to_data_without_login(self):
        self.client.logout()
        response = self.client.get(reverse("detailed-task", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("lists"))
        self.assertEqual(response.status_code, 403)

    def test_create_task(self):
        task = {
            "title": "test_task",
            "description": "test_description",
            "comments": "test_comment",
            "difficulty": 1,
            "deadline": "2022-06-05",
        }
        response = self.client.post(reverse("task-create"), data=task)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(title="test_task").exists())

    def test_update_task(self):
        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user)
        task_id = tasks[2]

        task_update = {"is_active": False}

        response = self.client.patch(
            reverse("detailed-task", kwargs={"pk": task_id.id}),
            data=task_update,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        task = Task.objects.get(id=task_id.id)
        self.assertEqual(task.is_active, task_update["is_active"])

    def test_delete_task(self):
        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user)
        task_id = tasks[2]

        response = self.client.delete(
            reverse("detailed-task", kwargs={"pk": task_id.id})
        )
        self.assertEqual(response.status_code, 204)
        self.assertTrue(not Task.objects.filter(id=task_id.id).exists())

    def test_list_create(self):
        list = {
            "date_created": "2020-06-06",
        }
        response = self.client.post(reverse("list-create"), data=list)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(List.objects.filter(date_created=list["date_created"]).exists())
