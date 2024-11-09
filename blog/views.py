from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from blog.forms import BlogEntryForm
from blog.models import BlogEntry
from config.settings import DEFAULT_FROM_EMAIL


class BlogEntryListView(LoginRequiredMixin, ListView):
    model = BlogEntry

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Модератор продуктов"
        is_content_manager = self.request.user.groups.filter(name="Контент-менеджер").exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context['is_content_manager'] = is_content_manager
        return context


class AllBlogEntryListView(LoginRequiredMixin, ListView):
    model = BlogEntry
    template_name = "blog/blogentry_list.html"

    def dispatch(self, request, *args, **kwargs):

        # Проверка, состоит ли пользователь в группе "Контент-менеджер"
        is_content_manager = self.request.user.groups.filter(name="Контент-менеджер").exists()

        if is_content_manager:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("У вас нет доступа к этой странице.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Модератор продуктов"
        is_content_manager = self.request.user.groups.filter(name="Контент-менеджер").exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context['is_content_manager'] = is_content_manager
        return context


class MyBlogEntryListView(LoginRequiredMixin, ListView):
    model = BlogEntry
    template_name = "blog/blogentry_list.html"

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(author=user)


class BlogEntryCreateView(LoginRequiredMixin, CreateView):
    # Модель куда выполняется сохранение
    model = BlogEntry
    # Класс на основе которого будет валидация полей
    form_class = BlogEntryForm

    success_url = reverse_lazy("blog:blogentry_list")

    def form_valid(self, form):
        blog_entry = form.save()
        user = self.request.user
        blog_entry.author = user
        blog_entry.save()
        return super().form_valid(form)


class BlogEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    success_url = reverse_lazy("blog:blogentry_list")

    def get_success_url(self):
        return reverse("blog:blogentry_detail", args=[self.kwargs.get("pk")])

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект записи
        blog_entry = super().get_object()
        # Проверяем, является ли текущий пользователь автором записи
        if blog_entry.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Вы не можете изменять эту запись.")


class BlogEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogEntry
    success_url = reverse_lazy("blog:blogentry_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект записи
        blog_entry = super().get_object()
        # Проверяем, является ли текущий пользователь автором записи
        if blog_entry.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Вы не можете удалять эту запись.")


class BlogEntryDetailView(LoginRequiredMixin, DetailView):
    model = BlogEntry

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        if self.object.view_count == 100:
            subject = f"{self.object.title} - Количество просмотров достигло 100!"
            message = f"Поздравляю, статья {self.object.title} ОООЧЕНЬ популярна!!!"
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = ["k.s.barkhatov@gmail.com"]
            send_mail(subject, message, from_email, recipient_list)
        self.object.save()
        return self.object


class SendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        subject = "Hello from Django"
        message = "This is a test email sent from a Django application."
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = ["k.s.barkhatov@gmail.com"]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponse("Email sent successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")


class BlogEntryUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        blog_entry = get_object_or_404(BlogEntry, pk=pk)

        if request.user.has_perm("blog.can_unpublish_blogentry"):
            # Логика снятия с публикации
            blog_entry.is_published = False
            blog_entry.save()
            return redirect("blog:all_blogentry_list")

        if blog_entry.author == self.request.user:
            # Логика снятия с публикации
            blog_entry.is_published = False
            blog_entry.save()
            return redirect("blog:blogentry_list")

        return HttpResponseForbidden("У вас нет прав для снятия записи с публикации")


class BlogEntryPublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        blog_entry = get_object_or_404(BlogEntry, pk=pk)

        if request.user.has_perm("blog.can_unpublish_blogentry"):
            # Логика снятия с публикации
            blog_entry.is_published = True
            blog_entry.save()
            return redirect("blog:all_blogentry_list")

        if blog_entry.author == self.request.user:
            # Логика снятия с публикации
            blog_entry.is_published = True
            blog_entry.save()
            return redirect("blog:blogentry_list")

        return HttpResponseForbidden("У вас нет прав для публикации этой записи")
