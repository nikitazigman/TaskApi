from django.urls import path

from .views import ListLists, DetailList, ListTask, DetailedTask


urlpatterns = [
    path('lists/', ListLists.as_view()),
    path('list/<int:pk>/', DetailList.as_view()),
    path('tasks/', ListTask.as_view()),
    path('task/<int:pk>', DetailedTask.as_view()),
]

