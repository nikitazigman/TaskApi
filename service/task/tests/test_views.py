from django.core.management import call_command
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from task.models import Task
from task.serializers import TaskSerializer
from user.models import WorkBalancerUser


class TaskViewTestCase(TestCase):
    users: QuerySet[WorkBalancerUser]

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("generate_test_data")
        cls.users = WorkBalancerUser.objects.all()

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(
            user=WorkBalancerUser.objects.get(username=self.users[0].username)
        )

    def test_get_user_task_list(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)

        user_tasks_models = Task.objects.filter(user__username=self.users[0].username)
        serializer = TaskSerializer(user_tasks_models, many=True)
        for response_task, model_task in zip(response.json(), serializer.data):
            self.assertDictEqual(response_task, dict(model_task))

    def test_get_filtered_task_list_by_deadline(self) -> None:
        expected_tasks = Task.objects.filter(
            user__username=self.users[0].username
        ).exclude(deadline=None)

        response = self.client.get(
            reverse("task-list"), {"deadline": str(expected_tasks[0].deadline)}
        )
        self.assertEqual(response.status_code, 200)

        serializer = TaskSerializer(expected_tasks, many=True)
        for response_task, model_task in zip(response.json(), serializer.data):
            self.assertDictEqual(response_task, dict(model_task))

    def test_get_filtered_task_list_by_completed(self) -> None:
        expected_tasks = Task.objects.filter(
            user__username=self.users[0].username, completed_at=None
        )

        response = self.client.get(reverse("task-list"), {"completed": False})

        self.assertEqual(response.status_code, 200)

        serializer = TaskSerializer(expected_tasks, many=True)
        for response_task, model_task in zip(response.json(), serializer.data):
            self.assertDictEqual(response_task, dict(model_task))

    def test_get_detailed_task(self) -> None:
        expected_task = Task.objects.filter(user__username=self.users[0].username).first()

        response = self.client.get(
            reverse("task-detail", kwargs={"pk": expected_task.id})
        )

        self.assertEqual(response.status_code, 200)

        serializer = TaskSerializer(expected_task)
        self.assertDictEqual(response.json(), dict(serializer.data))

    def test_cannot_get_task_of_other_user(self) -> None:
        expected_task = Task.objects.filter(user__username=self.users[1].username).first()

        response = self.client.get(
            reverse("task-detail", kwargs={"pk": expected_task.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_create_task(self) -> None:
        new_task = {
            "title": "new_task",
            "level": 1,
            "deadline": None,
            "completed": False,
            "day": [],
        }
        response = self.client.post(
            reverse("task-list"),
            data=new_task,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        returned_task = response.json()
        self.assertIn("id", returned_task)
        self.assertTrue(Task.objects.filter(id=returned_task["id"]).count())

        task_user = Task.objects.get(id=returned_task["id"]).user
        client_user = WorkBalancerUser.objects.get(username=self.users[0].username)
        self.assertEqual(task_user.id, client_user.id)

    def test_update_task(self) -> None:
        test_title = "test_new_title"
        test_task = Task.objects.filter(user__username=self.users[0].username).first()
        serializer = TaskSerializer(test_task)
        test_task_dict = dict(serializer.data)
        test_task_dict["title"] = test_title

        response = self.client.patch(
            reverse("task-detail", kwargs={"pk": test_task.id}),
            data=test_task_dict,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        returned_task = response.json()
        self.assertIn("id", returned_task)
        self.assertEqual(returned_task["id"], test_task.id)
        test_task.refresh_from_db()
        self.assertEqual(test_task.title, test_title)

    def test_partial_update_task(self) -> None:
        test_title = "test_new_title"
        test_task = Task.objects.filter(user__username=self.users[0].username).first()

        response = self.client.put(
            reverse("task-detail", kwargs={"pk": test_task.id}),
            data={"title": test_title},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        returned_task = response.json()
        self.assertIn("id", returned_task)
        self.assertEqual(returned_task["id"], test_task.id)
        test_task.refresh_from_db()
        self.assertEqual(test_task.title, test_title)

    def test_delete_task(self) -> None:
        test_task = Task.objects.filter(user__username=self.users[0].username).first()
        response = self.client.delete(reverse("task-detail", kwargs={"pk": test_task.id}))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.filter(id=test_task.id).count(), 0)
