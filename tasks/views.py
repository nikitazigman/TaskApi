import logging

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import List, Task
from .serializers import ListSerializer, TaskSerializer, ListCreateSerializer, TaskCreateSerializer
from .filters import TaskFilterSet, UserFilterSet


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ListList(generics.ListAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet


class ListCreate(generics.CreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilterSet


class TaskCreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class TaskDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet
