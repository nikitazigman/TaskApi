from rest_framework import serializers
from . import models


class DaySerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        exclude = ["user"]
