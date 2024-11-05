from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from catalog.forms import StyleFormMixin

from .models import CustomUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    """Кастомная форма для создания пользователя"""

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Ваш пароль"  # Меняем label для password1
        self.fields["password2"].label = (
            "Повторите пароль"  # Меняем label для password2
        )

        self.fields["password1"].help_text = (
            "- Ваш пароль не должен быть слишком похож на другую личную информацию.<br>"
            "- Ваш пароль должен содержать как минимум 8 символов.<br>"
            "- Ваш пароль не должен быть распространённым.<br>"
            "- Ваш пароль не должен состоять только из цифр."
        )

        self.fields["password2"].help_text = "Введите тот же пароль для подтверждения."


class CustomUserUpdateForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["avatar", "country"]


# User = get_user_model()

# class CustomUserChangeForm(forms.ModelForm):
#     """Форма для редактирования данных пользователя с добавлением смены пароля"""
#
#     current_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         label='Текущий пароль',
#         required=False  # Это поле будет необязательным
#     )
#     new_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         label='Новый пароль',
#         required=False  # Это поле будет необязательным
#     )
#     confirm_new_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         label='Подтверждение нового пароля',
#         required=False  # Это поле будет необязательным
#     )
#
#     class Meta:
#         model = User
#         fields = ['email', 'phone_number', 'avatar', 'country']
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
#             raise ValidationError("Этот email уже используется.")
#         return email
#
#     def clean(self):
#         cleaned_data = super().clean()
#
#         # Логика для проверки пароля
#         current_password = cleaned_data.get('current_password')
#         new_password = cleaned_data.get('new_password')
#         confirm_new_password = cleaned_data.get('confirm_new_password')
#
#         if current_password or new_password or confirm_new_password:
#             # Если хотя бы одно из полей пароля заполнено
#             if not current_password:
#                 raise ValidationError({'current_password': 'Поле "Текущий пароль" обязательно для заполнения.'})
#             if new_password != confirm_new_password:
#                 raise ValidationError({'confirm_new_password': 'Новый пароль и подтверждение пароля не совпадают.'})
#
#             # Проводим проверку текущего пароля
#             user = self.instance
#             if not user.check_password(current_password):
#                 raise ValidationError({'current_password': 'Неверный текущий пароль.'})
#
#             # Устанавливаем новый пароль
#             user.set_password(new_password)
#             user.save()
#
#         return cleaned_data
