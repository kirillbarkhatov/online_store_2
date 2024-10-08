from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Contact, Product


# Create your views here.
def home(request):

    # вывод в консоль 5 последних созданных продуктов
    products = Product.objects.all().order_by("-created_at")[:5]
    for product in products:
        print(product.name)

    products = Product.objects.all()
    context = {"products": products}

    return render(request, "catalog/home.html", context)


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
