from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task.models import Task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name", "description", "deadline", "priority", "task_type",
            "assignees",
        ]
        widgets = {
            "deadline": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }


class TaskUpdateForm(TaskForm):
    class Meta(TaskForm.Meta):
        fields = TaskForm.Meta.fields + ["is_completed"]
