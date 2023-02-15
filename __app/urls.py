from django.urls import path

from .views import TaskCreate, TaskDetailed, TaskList

urlpatterns = [
    path("task/list/", TaskList.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailed.as_view(), name="task-detailed"),
    path("task/create/", TaskCreate.as_view(), name="task-create"),
]
