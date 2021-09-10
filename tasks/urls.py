from django.urls import path

from .views import ListList, ListDetail, TaskList, TaskDetailed


urlpatterns = [
    path('lists/', ListList.as_view(), name='lists'),
    path('list/<int:pk>/', ListDetail.as_view(), name='detailed-list'),
    path('tasks/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailed.as_view(), name='detailed-task'),
]

