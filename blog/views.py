from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from blog.forms import BlogEntryForm
from blog.models import BlogEntry


class BlogEntryListView(ListView):
    model = BlogEntry

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


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

    def get_success_url(self):
        return reverse("blog:blogentry_detail", args=[self.kwargs.get("pk")])


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    success_url = reverse_lazy("blog:blogentry_list")


class BlogEntryDetailView(DetailView):
    model = BlogEntry

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        if self.object.view_count == 100:
            subject = f"{self.object.title} - Количество просмотров достигло 100!"
            message = f"Поздравляю, статья {self.object.title} ОООЧЕНЬ популярна!!!"
            from_email = "barchatovkirill@mail.ru"
            recipient_list = ["k.s.barkhatov@gmail.com"]
            send_mail(subject, message, from_email, recipient_list)
        self.object.save()
        return self.object


class SendEmailView(View):
    def get(self, request):
        subject = "Hello from Django"
        message = "This is a test email sent from a Django application."
        from_email = "barchatovkirill@mail.ru"
        recipient_list = ["k.s.barkhatov@gmail.com"]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponse("Email sent successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
