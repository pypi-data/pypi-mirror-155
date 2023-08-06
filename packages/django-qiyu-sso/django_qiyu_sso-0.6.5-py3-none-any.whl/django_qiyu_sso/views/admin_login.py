from django.urls import reverse
from django.views.generic import RedirectView

__all__ = ["AdminLoginView"]


class AdminLoginView(RedirectView):
    """
    管理员登录的 hook 视图

    使用方式:

    >>> from django.contrib import admin
    >>> assert isinstance(admin.site, admin.AdminSite)
    >>> admin.site.login = AdminLoginView.as_view()

    .. warning::

        注意:

        您必须把 urls.sso_urls 添加到 URL 配置的地址中
    """

    def get_redirect_url(self, *args, **kwargs) -> str:
        login_url = reverse("login")  # login 配置必须是登录的地址
        next_url = self.request.GET.get("next", "/")
        return f"{login_url}?next={next_url}"
