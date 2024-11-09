from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда создания тестовых пользователей"""

    def handle(self, *args, **options):

        User = get_user_model()

        try:
            group = Group.objects.get(name="Модератор продуктов")
        except ObjectDoesNotExist:
            group = Group.objects.create(name="Модератор продуктов")
            unpublish_product_permission = Permission.objects.get(
                codename="can_unpublish_product"
            )
            delete_product_permission = Permission.objects.get(
                codename="delete_product"
            )
            group.permissions.add(
                unpublish_product_permission, delete_product_permission
            )
            group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно создана группа {group.name} c правами "{unpublish_product_permission}" и "{delete_product_permission}"'
                )
            )

        # создание модератора
        try:
            user = User.objects.get(email="moderator@moderator.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="moderator@moderator.ru",
        )
        user.set_password("123qwe456rty")
        user.groups.add(group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан модератор с email {user.email} с паролем 123qwe456rty и добавлен в группу {group.name}"
            )
        )

        try:
            group = Group.objects.get(name="Контент-менеджер")
        except ObjectDoesNotExist:
            group = Group.objects.create(name="Контент-менеджер")
            unpublish_blogentry_permission = Permission.objects.get(
                codename="can_unpublish_blogentry"
            )
            delete_blogentry_permission = Permission.objects.get(
                codename="delete_blogentry"
            )
            group.permissions.add(
                unpublish_blogentry_permission, delete_blogentry_permission
            )
            group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно создана группа {group.name} c правами "{unpublish_blogentry_permission}" и "{delete_blogentry_permission}"'
                )
            )

        # создание контент-менеджера
        try:
            user = User.objects.get(email="content@manager.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="content@manager.ru",
        )
        user.set_password("123qwe456rty")
        user.groups.add(group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан контент-менеджер с email {user.email} с паролем 123qwe456rty и добавлен в группу {group.name}"
            )
        )

        # создание тестового юзера №1
        try:
            user = User.objects.get(email="test1@test1.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="test1@test1.ru",
        )
        user.set_password("123qwe456rty")
        # user.groups.add(group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан тестовый пользователь с email {user.email} с паролем 123qwe456rty "
            )
        )

        # создание тестового юзера №2
        try:
            user = User.objects.get(email="test2@test2.ru").delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email="test2@test2.ru",
        )
        user.set_password("123qwe456rty")
        # user.groups.add(group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан тестовый пользователь с email {user.email} с паролем 123qwe456rty "
            )
        )
