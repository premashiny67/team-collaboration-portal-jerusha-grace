import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a temporary Render administrator account."

    def handle(self, *args, **options):
        if os.environ.get("RENDER_ADMIN_SETUP") != "1":
            self.stdout.write("Admin setup is disabled.")
            return

        username = os.environ.get("RENDER_ADMIN_USERNAME")
        email = os.environ.get("RENDER_ADMIN_EMAIL", "")
        password = os.environ.get("RENDER_ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError(
                "RENDER_ADMIN_USERNAME and RENDER_ADMIN_PASSWORD are required."
            )

        User = get_user_model()

        user, created = User.objects.get_or_create(
            **{User.USERNAME_FIELD: username},
            defaults={"email": email} if any(
                field.name == "email" for field in User._meta.fields
            ) else {},
        )

        if hasattr(user, "is_staff"):
            user.is_staff = True

        if hasattr(user, "is_superuser"):
            user.is_superuser = True

        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"Administrator account {action} successfully."
            )
        )
