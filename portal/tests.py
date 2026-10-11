from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Task, UserProfile

User = get_user_model()


class PortalPermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="portaladmin", email="admin@example.com", password="Test-pass-12345"
        )
        self.member = User.objects.create_user(
            username="member1", email="member@example.com", password="Test-pass-12345"
        )
        self.other_member = User.objects.create_user(
            username="member2", email="member2@example.com", password="Test-pass-12345"
        )
        self.task = Task.objects.create(
            title="Assigned task",
            assigned_to=self.member,
            created_by=self.admin,
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_member_cannot_open_admin_task_creation(self):
        self.client.login(username="member1", password="Test-pass-12345")
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 302)

    def test_member_cannot_update_another_members_task(self):
        self.client.login(username="member2", password="Test-pass-12345")
        response = self.client.post(
            reverse("task_status_update", args=[self.task.id]),
            {"status": Task.Status.COMPLETED},
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.TODO)

    def test_assigned_member_can_update_status(self):
        self.client.login(username="member1", password="Test-pass-12345")
        self.client.post(
            reverse("task_status_update", args=[self.task.id]),
            {"status": Task.Status.IN_PROGRESS},
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)

    def test_superuser_is_admin(self):
        self.client.login(username="portaladmin", password="Test-pass-12345")
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 200)
