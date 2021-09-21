import logging

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from .filters import TaskFilterSet, UserFilterSet


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ListList(generics.ListCreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilterSet


class TaskDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet
