from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig

from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogEntryListView.as_view(), name="blogentry_list"),
    # path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # path("product/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
    # path("product/create", views.ProductCreateView.as_view(), name="product_create"),
    # path("product/<int:pk>/update", views.ProductUpdateView.as_view(), name="product_update"),
    # path("product/<int:pk>/delete", views.ProductDeleteView.as_view(), name="product_delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
