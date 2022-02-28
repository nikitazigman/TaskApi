import logging
from datetime import timedelta
from typing import Union

from app.models import Day, Task
from app.serializers import DaySerializer, TaskSerializer
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from faker import Faker

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

        for _ in range(lists_number):
            day = Day.objects.create(user_id=user.id, date_created=date)

            for _ in range(tasks_in_list):
                Task.objects.create(
                    user_id=user.id,
                    title=self.fake.text(max_nb_chars=20),
                    description=self.fake.text(max_nb_chars=100),
                    comments=self.fake.text(max_nb_chars=100),
                    deadline=self.fake.date_between(start_date="-1y", end_date="+1y"),
                    day=day,
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
        self, response_json: dict, queryset: Union[Day, Task]
    ):
        serializer_type = {
            "Task": TaskSerializer,
            "Day": DaySerializer,
        }

        serializer = serializer_type[type(queryset.first()).__name__]

        for query_obj, resp_obj in zip(queryset, response_json):
            serialized_obj = serializer(query_obj)
            logger.debug(f"{serialized_obj.data['id']=} == {resp_obj['id']=}")
            self.assertEqual(serialized_obj.data, resp_obj)

    def test_get_user_lists(self):
        response = self.client.get(reverse("day-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.list_number)

        user = User.objects.get(username=self.username_one)
        days = Day.objects.filter(user_id=user.id)

        self.compare_response_with_queryset(response_json=response.json(), queryset=days)

    def test_get_user_detailed_lists(self):
        user = User.objects.get(username=self.username_one)
        days = Day.objects.filter(user_id=user.id)
        day_id = days[2].id

        response = self.client.get(reverse("task-list"), {"day": day_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.task_number_in_one_list)

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user.id, day=day_id)

        self.compare_response_with_queryset(response_json=response.json(), queryset=tasks)

    def test_get_user_tasks(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()),
            self.task_number_in_one_list * self.list_number,
        )

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user.id)

        self.compare_response_with_queryset(response_json=response.json(), queryset=tasks)

    def test_get_user_active_tasks(self):
        response = self.client.get(reverse("task-list"), {"completed": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()),
            self.task_number_in_one_list * self.list_number,
        )

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user.id, completed=False)

        self.compare_response_with_queryset(response_json=response.json(), queryset=tasks)

    def test_get_user_active_tasks_for_the_list(self):
        user = User.objects.get(username=self.username_one)
        days = Day.objects.filter(user_id=user.id)
        day_id = days[2].id

        deadline_after = timezone.now().date() + timedelta(days=2)

        response = self.client.get(
            reverse("task-list"),
            {
                "completed": False,
                "excluded_day": day_id,
                "deadline_after": str(deadline_after),
            },
        )

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(
            user_id=user.id,
            completed=False,
            deadline__gte=deadline_after,
        ).exclude(day=day_id)

        self.compare_response_with_queryset(response_json=response.json(), queryset=tasks)

    def test_get_user_detailed_task(self):
        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user.id)
        task_id = tasks[2].id

        response = self.client.get(reverse("task-detailed", kwargs={"pk": task_id}))
        self.assertEqual(response.status_code, 200)

        task = Task.objects.get(id=task_id)
        serialized_task = TaskSerializer(task)
        self.assertEqual(serialized_task.data, response.json())

    def test_cannot_get_task_of_other_user(self):

        user = User.objects.get(username=self.username_two)
        user_two_task = Task.objects.filter(user_id=user.id).first()
        task_id = user_two_task.id

        response = self.client.get(reverse("task-detailed", kwargs={"pk": task_id}))

        self.assertEqual(response.status_code, 404)

    def test_cannot_get_access_to_data_without_login(self):
        self.client.logout()
        response = self.client.get(reverse("task-detailed", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(reverse("day-list"))
        self.assertEqual(response.status_code, 401)

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
        tasks = Task.objects.filter(user_id=user.id)
        task_id = tasks[2]

        task_update = {"completed": True}

        response = self.client.patch(
            reverse("task-detailed", kwargs={"pk": task_id.id}),
            data=task_update,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        task = Task.objects.get(id=task_id.id)
        self.assertEqual(task.completed, task_update["completed"])

    def test_delete_task(self):
        user = User.objects.get(username=self.username_one)
        tasks = Task.objects.filter(user_id=user.id)
        task_id = tasks[2]

        response = self.client.delete(reverse("task-detailed", kwargs={"pk": task_id.id}))
        self.assertEqual(response.status_code, 204)
        self.assertTrue(not Task.objects.filter(id=task_id.id).exists())

    def test_list_create(self):
        day = {
            "date_created": "2020-06-06",
        }
        response = self.client.post(reverse("task-detailed"), data=day)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Day.objects.filter(date_created=day["date_created"]).exists())
