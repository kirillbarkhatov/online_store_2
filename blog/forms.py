from django.forms import ModelForm

from .models import BlogEntry


class BlogEntryForm(ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = BlogEntry
        # Включаем все поля с модели в форму
        fields = "__all__"
