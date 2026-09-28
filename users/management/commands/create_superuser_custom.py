"""Management command для создания суперпользователя."""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Создаёт суперпользователя с данными из .env."""

    help = 'Создаёт суперпользователя с данными из .env (SUPERUSER_*).'

    def handle(self, *args, **options):
        """Создаёт суперпользователя."""
        username = os.getenv('SUPERUSER_USERNAME', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'admin')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Пользователь "{username}" уже существует.')
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(
            self.style.SUCCESS(f'Суперпользователь "{username}" создан.')
        )
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Пароль: {password}')
