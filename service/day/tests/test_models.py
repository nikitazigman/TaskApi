from day.models import Day
from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from model_bakery import baker


class DayModelTestCase(TestCase):
    def test_date_and_user_is_unique(self) -> None:
        fake = Faker()
        test_date = fake.date()
        user = baker.make("user.WorkBalancerUser")
        with self.assertRaises(IntegrityError) as exc_inf:
            baker.make("day.Day", user=user, date=test_date, _quantity=2)

        self.assertIn("unique", str(exc_inf.exception))

    def test_ordering(self) -> None:
        quantity = 20
        fake = Faker()
        fake_dates = (fake.unique.date() for _ in range(quantity))
        baker.make("day.Day", date=fake_dates, _quantity=quantity)

        days = list(Day.objects.all())
        sorted_days = sorted(days, key=lambda day: day.date)

        self.assertEqual(days, sorted_days)
