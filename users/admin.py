from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Настройки отображения модели в админке"""

    list_display = ("id", "email")  # вывод колонок
