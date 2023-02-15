from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class DayViewSet(ModelViewSet):
    queryset = models.Day.objects.all()
    serializer_class = serializers.DaySerializer
    filterset_fields = ["date"]

    def perform_create(self, serializer: serializers.DaySerializer) -> None:
        serializer.save(user=self.request.user)
