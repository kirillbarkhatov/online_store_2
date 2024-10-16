from django.contrib import admin

from .models import BlogEntry


# Register your models here.
@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    """Настройки отображения модели в админке"""

    list_display = (
        "title",
        "short_content",
        "created_at",
        "is_published",
        "view_count",
    )  # вывод колонок
    search_fields = (
        "title",
        "content",
    )  # поиск по указанному полю/полям

    def short_content(self, obj):
        # Обрезаем текст до 50 символов и добавляем '...' если он длиннее
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "content"  # Название колонки в админке
