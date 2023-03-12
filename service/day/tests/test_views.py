from day.models import Day
from day.serializers import DaySerializer
from django.core.management import call_command
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from user.models import WorkBalancerUser


class DayViewTestCase(TestCase):
    users: "QuerySet[WorkBalancerUser]"

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("generate_test_data")
        cls.users = WorkBalancerUser.objects.all()

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(
            user=WorkBalancerUser.objects.get(username=self.users[0].username)
        )

    def test_get_users_days(self) -> None:
        days = Day.objects.filter(user__username=self.users[0].username)
        serializer = DaySerializer(days, many=True)
        expected_days = serializer.data

        response = self.client.get(reverse("day-list"))

        self.assertEqual(response.status_code, 200)
        returned_days = response.json()

        self.assertEqual(len(returned_days), len(expected_days))

        for returned_day, expected_day in zip(returned_days, expected_days):
            self.assertEqual(returned_day, dict(expected_day))
            self.assertIn("assigned_tasks", returned_day)
            self.assertIn("completed_tasks", returned_day)

    def test_can_filter_by_date(self) -> None:
        day = Day.objects.filter(user__username=self.users[0].username).first()
        serializer = DaySerializer(day)
        expected_day = serializer.data

        response = self.client.get(reverse("day-list"), data={"date": str(day.date)})

        self.assertEqual(response.status_code, 200)
        returned_day = response.json()

        self.assertEqual(len(returned_day), 1)

        self.assertEqual(returned_day[0], dict(expected_day))

    def test_get_detailed_day(self) -> None:
        day = Day.objects.filter(user__username=self.users[0].username).first()
        serializer = DaySerializer(day)
        expected_day = serializer.data

        response = self.client.get(reverse("day-detail", kwargs={"pk": day.id}))

        self.assertEqual(response.status_code, 200)
        returned_day = response.json()

        self.assertEqual(returned_day, dict(expected_day))
        self.assertIn("assigned_tasks", returned_day)
        self.assertIn("completed_tasks", returned_day)

    def test_cannot_get_day_of_other_user(self) -> None:
        day = Day.objects.filter(user__username=self.users[1].username).first()

        response = self.client.get(reverse("day-detail", kwargs={"pk": day.id}))

        self.assertEqual(response.status_code, 404)

    def test_create(self) -> None:
        new_day = {"date": "2023-02-01"}
        response = self.client.post(reverse("day-list"), data=new_day, format="json")

        self.assertEqual(response.status_code, 201)
        returned_day = response.json()

        self.assertIn("id", returned_day)
        self.assertTrue(Day.objects.filter(id=returned_day["id"]).count())

        day_user = Day.objects.get(id=returned_day["id"]).user
        client_user = WorkBalancerUser.objects.get(username=self.users[0].username)
        self.assertEqual(day_user.id, client_user.id)

    def test_create_if_exist(self) -> None:
        existing_day = Day.objects.filter(user=self.users[0]).first()
        if existing_day is None:
            raise ValueError()

        new_day = {
            "date": existing_day.date,
        }
        response = self.client.post(reverse("day-list"), data=new_day, format="json")

        self.assertEqual(response.status_code, 200)
        returned_day = response.json()

        self.assertIn("id", returned_day)
        self.assertEqual(existing_day.id, returned_day["id"])

    def test_update(self) -> None:
        test_date = "2020-01-01"

        test_day = Day.objects.filter(user__username=self.users[0].username).first()
        serializer = DaySerializer(test_day)
        test_day_dict = dict(serializer.data)
        test_day_dict["date"] = test_date

        response = self.client.patch(
            reverse("day-detail", kwargs={"pk": test_day.id}),
            data=test_day_dict,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        returned_day = response.json()
        self.assertIn("id", returned_day)
        self.assertEqual(returned_day["id"], test_day.id)

        test_day.refresh_from_db()
        self.assertEqual(str(test_day.date), test_date)

    def test_partially_update(self) -> None:
        test_date = "2020-01-01"

        test_day = Day.objects.filter(user__username=self.users[0].username).first()

        response = self.client.put(
            reverse("day-detail", kwargs={"pk": test_day.id}),
            data={"date": test_date},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        returned_day = response.json()
        self.assertIn("id", returned_day)
        self.assertEqual(returned_day["id"], test_day.id)

        test_day.refresh_from_db()
        self.assertEqual(str(test_day.date), test_date)

    def test_delete(self) -> None:
        test_day = Day.objects.filter(user__username=self.users[0].username).first()
        response = self.client.delete(reverse("day-detail", kwargs={"pk": test_day.id}))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Day.objects.filter(id=test_day.id).count(), 0)
