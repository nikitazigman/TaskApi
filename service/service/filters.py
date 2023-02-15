from django.db.models import QuerySet
from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend


class BelongToOwnerFilter(DjangoFilterBackend):
    def filter_queryset(self, request: HttpRequest, queryset: QuerySet, view):
        queryset = queryset.filter(user=request.user)
        return super().filter_queryset(request, queryset, view)
