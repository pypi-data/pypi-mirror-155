from django.apps import AppConfig

__all__ = ["DjangoQiyuSsoConfig"]


class DjangoQiyuSsoConfig(AppConfig):
    name = "django_qiyu_sso"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.verbose_name = "奇遇SSO"
