from rest_framework import serializers

from .models import Task
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "comments",
            "level",
            "deadline",
            "completed",
            "created_at",
            "date",
        ]
        validators = [
            UniqueTogetherValidator(
                Task.objects.all(),
                fields=["title", "deadline"],
            ),
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "comments",
            "level",
            "deadline",
            "date",
        ]
        validators = [
            UniqueTogetherValidator(
                Task.objects.all(),
                fields=["title", "deadline"],
            ),
        ]
