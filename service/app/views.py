import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .filters import TaskFilterSet, UserFilterSet
from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    RegisterSerializer,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilterSet


class TaskCreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=User.objects.get(id=self.request.user.id))


class TaskDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet
