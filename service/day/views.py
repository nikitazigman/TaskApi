from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class DayViewSet(ModelViewSet):
    queryset = models.Day.objects.all()
    serializer_class = serializers.DaySerializer
    filterset_fields = ["date"]

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def retrieve_object_if_exist(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> None | Response:
        if "date" not in request.data:
            return None

        if not self.get_queryset().filter(date=request.data["date"]).exists():
            return None

        day = self.get_queryset().get(date=request.data["date"])
        serializer = self.get_serializer(day)

        return Response(serializer.data)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """returns serialzied object if it is already exist"""

        response = self.retrieve_object_if_exist(request, *args, **kwargs)

        return response if response else super().create(request, *args, **kwargs)
