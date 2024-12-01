from django.forms import ModelForm

from catalog.forms import StyleFormMixin

from .models import BlogEntry


class BlogEntryForm(StyleFormMixin, ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = BlogEntry
        # Включаем все поля с модели в форму
        exclude = (
            "view_count",
            "author",
        )
