from rest_framework import serializers

from .models import Day, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "comments",
            "difficulty",
            "deadline",
            "completed",
            "created_at",
            "day",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "comments",
            "difficulty",
            "deadline",
            "day",
        ]


class DaySerializer(serializers.ModelSerializer):
    number_finished_tasks = serializers.SerializerMethodField()
    number_active_tasks = serializers.SerializerMethodField()

    def get_number_active_tasks(self, obj: Day):
        return obj.tasks.filter(completed=False).count()

    def get_number_finished_tasks(self, obj: Day):
        return obj.tasks.filter(completed=True).count()

    class Meta:
        model = Day
        fields = [
            "id",
            "date_created",
            "number_finished_tasks",
            "number_active_tasks",
        ]


class DayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = [
            "date_created",
        ]
