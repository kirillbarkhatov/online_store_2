from django.contrib import admin

from .models import Category, Contact, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки отображения модели в админке"""

    list_display = (
        "id",
        "name",
    )  # вывод колонок
    search_fields = ("name",)  # поиск по указанному полю/полям


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройки отображения модели в админке"""

    list_display = (
        "id",
        "name",
        "price",
        "category",
    )  # вывод колонок
    list_filter = ("category",)  # добавление фильтра по указанному полю
    search_fields = (
        "name",
        "description",
    )  # поиск по указанному полю/полям


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Настройки отображения модели в админке"""

    list_display = ("id", "first_name", "last_name", "email")  # вывод колонок
