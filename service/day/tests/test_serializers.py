from day.models import Day
from day.serializers import DaySerializer
from django.test import TestCase
from model_bakery import baker


class TaskSerializerTestCase(TestCase):
    def test_user_field_is_excluded(self):
        baker.make("day.Day")
        serializer = DaySerializer(Day.objects.first())
        self.assertNotIn("user", serializer.data)

    def test_data_fields(self):
        essential_fields = {"date"}

        baker.make("day.Day")

        serializer = DaySerializer(Day.objects.first())
        data_fields = set(serializer.data)

        self.assertTrue(essential_fields.issubset(data_fields))
