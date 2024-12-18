from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Category, Contact, Product
from catalog.services import products_by_category

# Create your views here.


class ProductCreateView(LoginRequiredMixin, CreateView):
    # Модель куда выполняется сохранение
    model = Product
    # Класс на основе которого будет валидация полей
    form_class = ProductForm

    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект продукта
        product = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем продукта
        if product.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Вы не можете изменять этот продукт.")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект продукта
        product = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем продукта
        if product.owner == self.request.user or request.user.has_perm(
            "catalog.delete_product"
        ):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Вы не можете удалить этот продукт.")


class ProductListView(ListView):
    model = Product
    paginate_by = 3

    def get_queryset(self):

        products = cache.get("products")
        if not products:
            products = Product.objects.all()
            cache.set("products", products, 60)

        products_last_5 = products.order_by("-created_at")[:5]
        for product in products_last_5:
            print(product.name)

        return products.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Модератор продуктов"
        is_moderator = self.request.user.groups.filter(
            name="Модератор продуктов"
        ).exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context["is_moderator"] = is_moderator
        categories = Category.objects.all()
        context["categories"] = categories

        return context


class ProductByCategoryListView(ListView):
    model = Product
    paginate_by = 3
    template_name = "catalog/product_by_category_list.html"

    def get_queryset(self):
        # Получаем ID категории из параметров GET
        category_id = self.request.GET.get("category")

        return products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Модератор продуктов"
        is_moderator = self.request.user.groups.filter(
            name="Модератор продуктов"
        ).exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context["is_moderator"] = is_moderator
        categories = Category.objects.all()
        context["categories"] = categories

        return context


class UserProductListView(ListView):
    model = Product
    paginate_by = 3
    template_name = "catalog/product_list.html"

    def get_queryset(self):
        # в теле класса не работает вывод в консоль - только так
        user = self.request.user

        return Product.objects.filter(owner=user.id)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden(
                "У вас нет прав для снятия продукта с публикации"
            )

        # Логика снятия с публикации
        product.is_published = False
        product.save()

        return redirect("catalog:product_list")


class ContactsView(LoginRequiredMixin, TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["contacts"] = Contact.objects.all()
        return context

    # не очень понял как это работает
    @staticmethod
    def post(request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"{name}, указанные Вами телефон и сообщение получены<br>Телефон: {phone}<br>Сообщение: {message}"
        )


# переписано под CBV по рекомендациям урока
# class AddProduct(CreateView):
#     # Модель куда выполняется сохранение
#     model = Product
#     # Класс на основе которого будет валидация полей
#     form_class = ProductForm
#     # Выведем все существующие записи на странице
#     extra_context = {"products": Product.objects.all()}
#     # Шаблон с помощью которого
#     # будут выводиться данные
#     template_name = "catalog/add_product.html"
#     # На какую страницу будет перенаправление
#     # в случае успешного сохранения формы
#     success_url = "/add_product/"


# ЛистВью в FBV - устаревшая реализация
# def home(request):
#
#     # вывод в консоль 5 последних созданных продуктов
#     products = Product.objects.all().order_by("-created_at")[:5]
#     for product in products:
#         print(product.name)
#
#     products_list = Product.objects.all()
#
#     paginator = Paginator(products_list, 3)
#     page_number = request.GET.get("page", 1)
#     products = paginator.page(page_number)
#
#     context = {"products": products}
#
#     return render(request, "catalog/home.html", context)


# FBV - устаревшая реализация
# def product(request, pk):
#
#     product = Product.objects.get(pk=pk)
#     context = {"product": product}
#
#     return render(request, "catalog/product.html", context)

# добавление продукта в FBV - не дописано сохранение картинки - устаревшая реализация
# def add_product(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         description = request.POST.get("description")
#         image = request.POST.get("image")
#         category = request.POST.get("category")
#         price = request.POST.get("price")
#         Product.objects.create(name=name, description=description, image=image, price=price)
#         return HttpResponse(
#             f"{name} - {description} - {image} - {category} - {price}"
#         )
#
#     categories = Category.objects.all()
#     context = {"categories": categories}
#     return render(request, "catalog/add_product.html", context)

# FBV - устаревшая реализация
# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         return HttpResponse(
#             f"{name}, указанные Вами телефон и сообщение получены<br>Телефон: {phone}<br>Сообщение: {message}"
#         )
#
#     queryset = Contact.objects.all()
#     context = {"contacts": queryset}
#     return render(request, "catalog/contacts.html", context)
