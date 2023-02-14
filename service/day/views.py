from rest_framework.viewsets import ModelViewSet
from . import models, serializers


class DayViewSet(ModelViewSet):
    queryset = models.Day.objects.all()
    serializer_class = serializers.DaySerilizer
