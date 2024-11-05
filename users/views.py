import secrets

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from config.settings import DEFAULT_FROM_EMAIL

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Приветствуем тебя на нашем сайте! Перейди, пожалуйста, по ссылке для подтверждения почты {url}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserChangeView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "registration/edit_profile.html"

    context_object_name = "form"

    def get_object(self):
        """Получаем текущего пользователя"""
        return self.request.user

    def form_valid(self, form):
        """Сохраняем изменения в профиле"""
        form.save()  # Сохраняем изменения
        messages.success(self.request, "Ваш профиль был успешно обновлён!")
        return redirect(
            "users:edit-profile"
        )  # Перенаправляем обратно на редактирование профиля

    def form_invalid(self, form):
        """Если форма не прошла валидацию, показываем ошибку"""
        messages.error(self.request, "Произошла ошибка при обновлении профиля.")
        return self.render_to_response(self.get_context_data(form=form))


# class EditProfileView(UpdateView):
#     """CBV для редактирования профиля пользователя"""
#
#     model = CustomUser
#     form_class = CustomUserChangeForm
#     template_name = 'registration/edit_profile.html'
#     context_object_name = 'form'
#
#     def get_object(self):
#         """Получаем текущего пользователя"""
#         return self.request.user
#
#     def form_valid(self, form):
#         """Сохраняем форму и меняем пароль, если он был изменен"""
#         # Проверим, был ли изменён пароль
#         current_password = form.cleaned_data.get('current_password')
#         new_password = form.cleaned_data.get('new_password')
#
#         # Если пароль был изменен, меняем его
#         if new_password:
#             self.object.set_password(new_password)
#             self.object.save()
#
#         # Сохраняем остальные изменения
#         form.save()
#         messages.success(self.request, "Ваш профиль был обновлён успешно.")
#
#         return redirect('users:edit_profile')  # Перенаправляем на страницу редактирования профиля
#
#     def form_invalid(self, form):
#         """Если форма не прошла валидацию, выводим сообщение об ошибке"""
#         messages.error(self.request, "Произошла ошибка при обновлении профиля.")
#         return self.render_to_response(self.get_context_data(form=form))


def email_verification(request, token):
    """Логика подтверждения почты"""

    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
