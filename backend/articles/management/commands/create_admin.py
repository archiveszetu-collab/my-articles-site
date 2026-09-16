import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update the administrator account."

    def handle(self, *args, **options):
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")
        if not password:
            raise CommandError("DJANGO_ADMIN_PASSWORD is required.")

        username = os.environ.get("DJANGO_ADMIN_USERNAME", "admin")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "admin@example.com")
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        message = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Admin user {message}: {username}"))