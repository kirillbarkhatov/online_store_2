from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from catalog.forms import StyleFormMixin

class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    """Кастомная форма для создания пользователя"""

    # password1 = forms.CharField(
    #     label="Ваш пароль",)

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Ваш пароль"  # Меняем label для password1
        self.fields['password2'].label = "Повторите пароль"  # Меняем label для password2

        self.fields['password1'].help_text = (
                    "- Ваш пароль не должен быть слишком похож на другую личную информацию.<br>"
                    "- Ваш пароль должен содержать как минимум 8 символов.<br>"
                    "- Ваш пароль не должен быть распространённым.<br>"
                    "- Ваш пароль не должен состоять только из цифр."
                )

        self.fields['password2'].help_text = "Введите тот же пароль для подтверждения."
