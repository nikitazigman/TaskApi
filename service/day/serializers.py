from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField
from task.models import Task

from . import models


class DaySerializer(serializers.ModelSerializer):
    completed_tasks: "PrimaryKeyRelatedField[Task]" = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    assigned_tasks: "PrimaryKeyRelatedField[Task]" = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = models.Day
        exclude = ["user"]
