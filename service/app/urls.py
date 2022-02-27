from django.urls import path

from .views import DayCreate, DayList, TaskCreate, TaskDetailed, TaskList

urlpatterns = [
    path("day/list", DayList.as_view(), name="day-list"),
    path("day/create", DayCreate.as_view(), name="task-detailed"),
    path("task/list", TaskList.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailed.as_view(), name="task-detailed"),
    path("task/create", TaskCreate.as_view(), name="task-create"),
]
