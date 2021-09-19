import logging

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from . import logics
from .filters import TaskFilterSet


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ListList(generics.ListAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset)

        return super().get_queryset()


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilterSet

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset)

        return super().get_queryset()


class TaskDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset)
        return super().get_queryset()