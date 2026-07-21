from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task.models import Task, TaskType


class PublicTaskTests(TestCase):
    def test_login_required_for_dashboard(self):
        response = self.client.get(reverse("task:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={reverse('task:index')}")


class PrivateTaskTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testworker",
            password="password123",
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(name="Bugfix")
        self.task = Task.objects.create(
            name="Fix login button",
            description="Fix button UI",
            deadline=date(2026, 7, 30),
            priority="High",
            task_type=self.task_type,
        )

    def test_dashboard_accessible_for_logged_in_user(self):
        response = self.client.get(reverse("task:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task/index.html")

    def test_task_list_page_accessible(self):
        response = self.client.get(reverse("task:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task/task_list.html")

    def test_task_str_method(self):
        self.assertEqual(str(self.task), "Fix login button")
