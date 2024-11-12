from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig

from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("category/", views.ProductByCategoryListView.as_view(), name="product_by_category_list"),
    path("my-products/", views.UserProductListView.as_view(), name="user_product_list"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>", cache_page(60)(views.ProductDetailView.as_view()), name="product_detail"),
    path("product/create", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>/update",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product/<int:pk>/delete",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "product/<int:pk>/unpublish",
        views.ProductUnpublishView.as_view(),
        name="product_unpublish",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
