# Generated by Django 5.1.1 on 2024-10-14 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("content", models.TextField(verbose_name="Содержимое")),
                (
                    "preview",
                    models.ImageField(
                        blank=True, null=True, upload_to="blog", verbose_name="Превью"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(verbose_name="Отметьте для публикации"),
                ),
                (
                    "view_count",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
            ],
            options={
                "verbose_name": "Запись",
                "verbose_name_plural": "Записи",
                "ordering": ["created_at"],
            },
        ),
    ]