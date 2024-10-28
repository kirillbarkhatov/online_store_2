from django.forms import ModelForm

from .models import BlogEntry
from catalog.forms import StyleFormMixin


class BlogEntryForm(StyleFormMixin, ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = BlogEntry
        # Включаем все поля с модели в форму
        exclude = ("view_count",)
