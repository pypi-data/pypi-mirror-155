from django.conf import settings

QI_YU_SSO_CLIENT_ID = getattr(settings, "QI_YU_SSO_CLIENT_ID", None)
QI_YU_SSO_CLIENT_SECRET = getattr(settings, "QI_YU_SSO_CLIENT_SECRET", None)
QI_YU_SSO_REDIRECT_URI = getattr(settings, "QI_YU_SSO_REDIRECT_URI", None)

# 登录之后默认跳转的页面
QI_YU_SSO_INDEX_URI = getattr(settings, "QI_YU_SSO_INDEX_URI", "/")

# 退出登录的 URL
QI_YU_SSO_LOGOUT_URI = getattr(settings, "QI_YU_SSO_LOGOUT_URI", None)

QI_YU_LOGIN_URI = getattr(
    settings, "QI_YU_LOGIN_URI", "https://user.qiyutech.tech/oauth/authorize/"
)
QI_YU_TOKEN_URI = getattr(
    settings, "QI_YU_TOKEN_URI", "https://user.qiyutech.tech/oauth/token/"
)
QI_YU_USER_INFO_URI = getattr(
    settings, "QI_YU_USER_INFO_URI", "https://user.qiyutech.tech/api/user/info"
)

QI_YU_SSO_SCOPE = getattr(
    settings, "QI_YU_SSO_SCOPE", "read email mobile staff_status admin_status"
)
