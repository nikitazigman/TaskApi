import logging

from rest_framework import generics
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ListLists(generics.ListAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class DetailList(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        self.queryset = Task.objects.filter(list_id=self.kwargs['pk'], user_id=self.request.user)
        logger.debug(f"list_id={self.kwargs['pk']}, tasks_list={self.queryset}, user_id={self.request.user.id}")
        return super(DetailList, self).get_queryset()


class ListTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class DetailedTask(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
