from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views import generic

from task.forms import TaskForm, TaskUpdateForm
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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_completed=False)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


@login_required
def mark_task_completed(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.get(id=pk)
    if (not task.is_completed and (request.user in task.assignees.all()
                                   or request.user.position == "Admin")):
        task.is_completed = True
        task.save()
    return HttpResponseRedirect(reverse_lazy("task:task-detail", args=[pk]))


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task:task-list")

    def test_func(self):
        task = self.get_object()
        user = self.request.user
        is_assignee = user in task.assignees.all()
        is_admin = user.position == "Admin"
        return is_assignee or is_admin


class TaskDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Task
    success_url = reverse_lazy("task:task-list")

    def test_func(self):
        task = self.get_object()
        user = self.request.user
        is_assignee = user in task.assignees.all()
        is_admin = user.position == "Admin"
        return is_assignee or is_admin
