from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpRequest
from django.db.models import QuerySet


class BelongToOwnerFilter(DjangoFilterBackend):
    def filter_queryset(self, request: HttpRequest, queryset: QuerySet, view):
        queryset = queryset.filter(user=request.user)
        return super().filter_queryset(request, queryset, view)
