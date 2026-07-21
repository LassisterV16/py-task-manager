from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views import generic

from task.forms import (
    TaskForm,
    TaskUpdateForm,
    TaskNameSearchForm,
    WorkerNameUsernameSearchForm
)
from task.models import Task, Worker


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        context["num_tasks"] = Task.objects.count()
        context["num_workers"] = Worker.objects.count()
        context["completed_tasks"] = Task.objects.filter(
            is_completed=True
        ).count()
        context["tasks_in_progress"] = Task.objects.filter(
            is_completed=False, deadline__gte=today
        ).count()
        context["failed_deadlines"] = Task.objects.filter(
            is_completed=False, deadline__lt=today
        ).count()

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task/task_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_completed=False
        ).select_related("task_type").prefetch_related("assignees")

        tag = self.request.GET.get("tag", "")
        if tag:
            queryset = queryset.filter(
                tags__name=tag
            )

        form = TaskNameSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskMarkCompletedView(LoginRequiredMixin, generic.View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, id=pk)
        user = request.user
        is_assignee = task.assignees.filter(id=user.id).exists()
        is_admin = user.is_admin

        if not task.is_completed and (is_assignee or is_admin):
            task.is_completed = True
            task.save()
        return HttpResponseRedirect(
            reverse_lazy("task:task-detail", args=[pk])
        )


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

    def get_success_url(self):
        return self.request.GET.get("next") or reverse_lazy("task:task-list")

    def test_func(self):
        task = self.get_object()
        user = self.request.user
        return task.assignees.filter(id=user.id).exists() or user.is_admin


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
        return task.assignees.filter(id=user.id).exists() or user.is_admin


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    context_object_name = "worker_list"
    template_name = "task/worker_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = WorkerNameUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerNameUsernameSearchForm(
            initial={"username": username}
        )
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("tasks")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        non_completed_tasks = self.object.tasks.filter(
            is_completed=False
        )
        completed_tasks = self.object.tasks.filter(
            is_completed=True
        )

        context["active_tasks"] = non_completed_tasks
        context["completed_tasks"] = completed_tasks
        return context
