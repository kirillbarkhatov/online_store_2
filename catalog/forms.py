from django.forms import ModelForm

from .models import Product


class ProductForm(ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = Product
        # Включаем все поля с модели в форму
        fields = "__all__"
