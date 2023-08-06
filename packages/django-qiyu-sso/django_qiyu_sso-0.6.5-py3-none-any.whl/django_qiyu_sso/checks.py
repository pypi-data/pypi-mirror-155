from django.core import checks


# noinspection PyUnusedLocal
@checks.register("django_qiyu_sso")
def check_config(*args, **kwargs):
    """
    检测配置是否有效
    """
    from . import settings

    if settings.QI_YU_SSO_CLIENT_ID is None:
        checks.Error("QI_YU_SSO_CLIENT_ID is missing")

    if settings.QI_YU_SSO_CLIENT_SECRET is None:
        checks.Error("QI_YU_SSO_CLIENT_SECRET is missing")

    if settings.QI_YU_SSO_REDIRECT_URI is None:
        checks.Error("QI_YU_SSO_REDIRECT_URI is missing")
