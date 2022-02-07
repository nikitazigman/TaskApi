from rest_framework import serializers

from .models import List, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "comments",
            "difficulty",
            "deadline",
            "list_id",
        ]


class ListSerializer(serializers.ModelSerializer):
    number_finished_tasks = serializers.SerializerMethodField()
    number_active_tasks = serializers.SerializerMethodField()

    def get_number_active_tasks(self, obj: List):
        return obj.tasks.filter(is_active=True).count()

    def get_number_finished_tasks(self, obj: List):
        return obj.tasks.filter(is_active=False).count()

    class Meta:
        model = List
        fields = "__all__"


class ListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = [
            "date_created",
        ]
