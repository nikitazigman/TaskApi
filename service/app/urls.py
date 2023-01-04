from django.urls import path

from .views import TaskCreate, TaskDetailed, Register, TaskList

urlpatterns = [
    path("register/", Register.as_view(), name="registeration"),
    path("task/list/", TaskList.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailed.as_view(), name="task-detailed"),
    path("task/create/", TaskCreate.as_view(), name="task-create"),
]
