from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from blog.models import BlogEntry


class BlogEntryListView(ListView):
    model = BlogEntry

