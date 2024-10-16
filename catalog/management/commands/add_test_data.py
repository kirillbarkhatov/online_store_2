from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product
from blog.models import BlogEntry


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
        self.stdout.write(self.style.SUCCESS("Записи блога загружены из фикстур успешно"))

