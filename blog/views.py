from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.forms import BlogEntryForm
from blog.models import BlogEntry


class BlogEntryListView(ListView):
    model = BlogEntry


class BlogEntryCreateView(CreateView):
    # Модель куда выполняется сохранение
    model = BlogEntry
    # Класс на основе которого будет валидация полей
    form_class = BlogEntryForm

    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryUpdateView(UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryDetailView(DetailView):
    model = BlogEntry