from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import BlogEntry
from catalog.models import Category, Product
from users.models import CustomUser


class Command(BaseCommand):
    help = "Добавление данных из фикстур"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Category.objects.all().delete()
        Product.objects.all().delete()
        BlogEntry.objects.all().delete()

        # Добавляем данные из фикстур
        call_command("loaddata", "categories_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Категории загружены из фикстур успешно"))
        call_command("loaddata", "products_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Продукты загружены из фикстур успешно"))
        call_command("loaddata", "blogentry_fixture.json", format="json")
        self.stdout.write(
            self.style.SUCCESS("Записи блога загружены из фикстур успешно")
        )

        # создаем тестовых пользователей
        call_command("create_test_users")

        # распределяем владельцев
        smartphones = Product.objects.filter(category=1)
        blog_entries = BlogEntry.objects.all()
        smartphones_owner = CustomUser.objects.get(email="test1@test1.ru")
        smartphones.update(owner=smartphones_owner)
        blog_entries.update(author=smartphones_owner)

        self.stdout.write(
            self.style.SUCCESS(
                f"Владельцем продуктов категории Смартфоны назначен пользователь {smartphones_owner.email}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Автором всех записей в блоге назначен пользователь {smartphones_owner.email}"
            )
        )

        other_products = Product.objects.exclude(category=1)
        other_products_owner = CustomUser.objects.get(email="test2@test2.ru")
        other_products.update(owner=other_products_owner)

        self.stdout.write(
            self.style.SUCCESS(
                f"Владельцем продуктов в остальных категориях назначен пользователь {other_products_owner.email}"
            )
        )
