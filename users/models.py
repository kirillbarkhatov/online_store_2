from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    # прикрутить django-phonenumber-field
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар пользователя")
    # прикрутить django-countries
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
