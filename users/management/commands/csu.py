from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда создания суперпользователя"""

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.get(email="admin@admin.ru").delete()
        user = User.objects.create(
            email="admin@admin.ru",
        )
        user.set_password("123qwe456rty")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Успешно создан суперпользователь с email {user.email}")
        )
