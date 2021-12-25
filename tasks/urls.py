from django.urls import path

from .views import ListCreate, ListList, TaskCreate, TaskDetailed, TaskList

urlpatterns = [
    path("lists/", ListList.as_view(), name="lists"),
    path("list/create", ListCreate.as_view(), name="list-create"),
    path("tasks/", TaskList.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetailed.as_view(), name="detailed-task"),
    path("task/create", TaskCreate.as_view(), name="task-create"),
]
