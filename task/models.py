from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent"
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority,
        default=Priority.LOW
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def __str__(self):
        return self.name
