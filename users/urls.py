from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="catalog:product_list"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
