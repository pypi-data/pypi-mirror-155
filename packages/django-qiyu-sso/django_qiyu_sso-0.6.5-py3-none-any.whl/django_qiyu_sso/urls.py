"""
使用方法:

    urlpatterns += sso_urls

"""
from django.urls import path

from .views import OAuth2LoginView, LoginSuccessView, LogoutView

__all__ = ["sso_urls"]

sso_urls = [
    path("accounts/login/", OAuth2LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/login/success/", LoginSuccessView.as_view(), name="login_success"),
]
