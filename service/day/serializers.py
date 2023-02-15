from rest_framework import serializers

from . import models


class DaySerializer(serializers.ModelSerializer):
    completed_tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    assigned_tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Day
        exclude = ["user"]
