import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import TaskFilterSet, UserFilterSet
from .models import Day, Task
from .serializers import (DayCreateSerializer, DaySerializer,
                          TaskCreateSerializer, TaskSerializer)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DayList(generics.ListAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet


class DayCreate(generics.CreateAPIView):
    queryset = Day.objects.all()
    serializer_class = DayCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilterSet


class TaskCreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class TaskDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet
