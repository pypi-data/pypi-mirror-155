from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.views.generic import RedirectView

__all__ = ["LogoutView"]


class LogoutView(LoginRequiredMixin, RedirectView):
    """
    退出登录
    """

    url = "/"

    def get(self, request: HttpRequest, *args, **kwargs):
        logout(request=request)
        return super().get(request, *args, **kwargs)
