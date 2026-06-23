from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views import generic

from task.models import Task


@login_required
def index(request: HttpRequest) -> HttpResponse:
    today = timezone.localdate()

    num_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    tasks_in_progress = Task.objects.filter(
        is_completed=False, deadline__gte=today
    ).count()
    failed_deadlines = Task.objects.filter(
        is_completed=False, deadline__lt=today
    ).count()

    context = {
        "num_tasks": num_tasks,
        "completed_tasks": completed_tasks,
        "tasks_in_progress": tasks_in_progress,
        "failed_deadlines": failed_deadlines,
    }

    return render(request, "task/index.html", context=context)


class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_completed=False)



class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type", "assignees",)
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")
