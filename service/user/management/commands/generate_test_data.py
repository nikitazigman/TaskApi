from random import SystemRandom
from typing import Any

from day.models import Day
from django.core.management.base import BaseCommand, CommandParser
from django.utils.timezone import get_current_timezone
from faker import Faker
from model_bakery import baker
from user.models import WorkBalancerUser


class Command(BaseCommand):
    help = "generates dummy data in the db for test purpose only"  # noqa: VNE003, A003

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--users_quantity", type=int, default=10)
        parser.add_argument("--days_per_user", type=int, default=10)
        parser.add_argument("--max_tasks_per_day", type=int, default=20)

    def generate_tasks_for_the_day(
        self,
        days: list[Day],
        user: WorkBalancerUser,
        quantity: int,
        fake: Faker,
        max_tasks_per_day: int,
    ) -> None:
        for _ in range(quantity):
            assigned_days = list(
                {
                    self.random.choice(days)
                    for _ in range(self.random.randint(a=1, b=max_tasks_per_day))
                }
            )
            baker.make(
                "task.Task",
                days=assigned_days,
                deadline=fake.unique.date(),
                user=user,
                completed_at=self.random.choice(assigned_days)
                if self.random.choice((True, False))
                else None,
            )

    def handle(self, *args: Any, **options: Any) -> None | str:
        fake = Faker()
        self.random = SystemRandom()
        for wb_user in WorkBalancerUser.objects.exclude(username="admin").iterator():
            wb_user.delete()

        users_quantity = options["users_quantity"]
        days_per_user = options["days_per_user"]
        max_tasks_per_day = options["max_tasks_per_day"]

        users = [
            {"username": f"user_{i}", "password": f"test_password_{i}"}
            for i in range(users_quantity)
        ]

        for user in users:
            WorkBalancerUser.objects.create_user(**user)

        for wb_user in WorkBalancerUser.objects.all().iterator():
            unique_dates = (
                fake.unique.date_time(tzinfo=get_current_timezone())
                for _ in range(days_per_user)
            )
            days = baker.make(
                "day.Day", user=wb_user, date=unique_dates, _quantity=days_per_user
            )
            self.generate_tasks_for_the_day(
                days=days,
                user=wb_user,
                quantity=max_tasks_per_day,
                fake=fake,
                max_tasks_per_day=max_tasks_per_day,
            )

        return None
