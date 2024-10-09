from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView

from catalog.forms import ProductForm
from catalog.models import Contact, Product, Category


# Create your views here.
class AddProduct(CreateView):
    # Модель куда выполняется сохранение
    model = Product
    # Класс на основе которого будет валидация полей
    form_class = ProductForm
    # Выведем все существующие записи на странице
    extra_context = {'products': Product.objects.all()}
    # Шаблон с помощью которого
    # будут выводиться данные
    template_name = 'catalog/add_product.html'
    # На какую страницу будет перенаправление
    # в случае успешного сохранения формы
    success_url = '/add_product/'



def home(request):

    # вывод в консоль 5 последних созданных продуктов
    products = Product.objects.all().order_by("-created_at")[:5]
    for product in products:
        print(product.name)

    products_list = Product.objects.all()


    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page', 1)
    products = paginator.page(page_number)

    context = {"products": products}

    return render(request, "catalog/home.html", context)


def product(request, pk):

    product = Product.objects.get(pk=pk)
    context = {"product": product}

    return render(request, "catalog/product.html", context)


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


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"{name}, указанные Вами телефон и сообщение получены<br>Телефон: {phone}<br>Сообщение: {message}"
        )

    queryset = Contact.objects.all()
    context = {"contacts": queryset}
    return render(request, "catalog/contacts.html", context)
