import logging

from rest_framework import generics, permissions
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from . import logics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ListList(generics.ListAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset)

        return super().get_queryset()


class ListDetail(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset).filter(
            list_id=self.kwargs['pk'])

        return super().get_queryset()


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset)

        return super().get_queryset()


class TaskDetailed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        self.queryset = logics.filter_owner_data(user=self.request.user, queryset=self.queryset)
        return super().get_queryset()