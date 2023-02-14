from django.test import TestCase
from model_bakery import baker
from task.models import Task
from day.models import Day
from django.db import IntegrityError
from faker import Faker


class TaskTestCase(TestCase):
    def test_level_in_range_1_9(self) -> None:
        for level in range(1, 11):
            baker.make("task.Task", level=level)

    def test_deadline_can_be_null(self) -> None:
        baker.make("task.Task", deadline=None)

    def test_day_can_be_null(self) -> None:
        baker.make("task.Task", day=None)

    def test_completed_at_can_be_null(self) -> None:
        baker.make("task.Task", completed_at=None)

    def test_ordering(self) -> None:
        fake = Faker()
        random_dates = (fake.date() for _ in range(20))

        for random_date in random_dates:
            baker.make("task.Task", deadline=random_date)

        tasks = list(Task.objects.all())
        sorted_tasks = sorted(
            tasks, key=lambda task: task.deadline if task.deadline else 0
        )
        self.assertEqual(tasks, sorted_tasks)

    def test_level_constrains_negative_level(self) -> None:
        with self.assertRaises(IntegrityError):
            baker.make("task.Task", level=-1)

    def test_level_constrains_zero_level(self) -> None:
        with self.assertRaises(IntegrityError):
            baker.make("task.Task", level=0)

    def test_level_constrains_out_of_upper_limit_level(self) -> None:
        with self.assertRaises(IntegrityError):
            baker.make("task.Task", level=11)

    def test_day_cascade_delete(self) -> None:
        origin_quantity = 5
        baker.make("day.Day")
        day = Day.objects.first()
        baker.make("task.Task", day=day, _quantity=origin_quantity)

        self.assertEqual(Task.objects.filter(day=day).count(), origin_quantity)

        day.delete()
        self.assertEqual(Task.objects.filter(day=day).count(), 0)
