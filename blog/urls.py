from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig

from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogEntryListView.as_view(), name="blogentry_list"),
    # path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("<int:pk>", views.BlogEntryDetailView.as_view(), name="blogentry_detail"),
    path("create", views.BlogEntryCreateView.as_view(), name="blogentry_create"),
    path("<int:pk>/update", views.BlogEntryUpdateView.as_view(), name="blogentry_update"),
    path("<int:pk>/delete", views.BlogEntryDeleteView.as_view(), name="blogentry_delete"),
    path('send-email/', views.SendEmailView.as_view(), name='send_email'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
