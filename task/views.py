from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.shortcuts import render

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