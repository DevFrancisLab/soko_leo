from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, LogoutView, RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="token_logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
