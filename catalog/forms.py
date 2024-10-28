from django.forms.fields import BooleanField
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = Product
        # Включаем все поля с модели в форму
        fields = "__all__"

    def clean(self):
        # валидация данных нескольких полей
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        banned_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

        for banned_word in banned_words:
            if banned_word in name.lower() or banned_word in description.lower():
                raise ValidationError(f'Слово "{banned_word}" недопустимо в имени или описании товара')
        return cleaned_data

    def clean_price(self):
        # валидация данных в поле price
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price
