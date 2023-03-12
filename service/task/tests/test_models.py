from day.models import Day
from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from model_bakery import baker
from task.models import Task


class TaskTestCase(TestCase):
    def test_level_in_range_1_9(self) -> None:
        for level in range(1, 11):
            baker.make("task.Task", level=level)

    def test_deadline_can_be_null(self) -> None:
        baker.make("task.Task", deadline=None)

    def test_day_can_be_null(self) -> None:
        # * by default the baker creates empty field
        # * if null property of model was set to True
        baker.make("task.Task")

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

    def test_can_complete_the_task(self) -> None:
        day = baker.make(Day)
        task = baker.make(Task, completed_at=None, days=[day])

        task.completed = True
        self.assertEqual(task.completed_at.id, task.days.first().id)

    def test_undo_task_complete(self) -> None:
        day = baker.make(Day)
        task = baker.make(Task, completed_at=day, days=[day])

        self.assertTrue(task.completed)
        task.completed = False

        self.assertEqual(task.completed_at, None)
        self.assertFalse(task.completed)
