from django.urls import path

from task.views import index, TaskList, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("task-list/", TaskList.as_view(), name="task-list"),
    path("task-list/create/", TaskCreateView.as_view(), name="task-create"),
    path("task-list/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task-list/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]

app_name = "task"