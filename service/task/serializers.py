from rest_framework import serializers

from . import models


class TaskSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField(required=False)

    class Meta:
        model = models.Task
        exclude = ["user"]
