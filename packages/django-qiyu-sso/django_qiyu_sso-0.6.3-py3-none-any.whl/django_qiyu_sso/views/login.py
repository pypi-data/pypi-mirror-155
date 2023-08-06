import secrets
from urllib.parse import urlencode

from django.http import HttpRequest
from django.views.generic import RedirectView
from django_qiyu_utils import RedirectHelper
from qiyu_sso import QiYuSSOSync
from qiyu_sso.forms import LoginArgs
from qiyu_sso.helper import gen_code_verifier, compute_code_challenge

from .. import settings

__all__ = ["OAuth2LoginView"]


class OAuth2LoginView(RedirectView):
    """
    跳转到 OAuth2 登录的页面
    """

    def get_redirect_url(self, *args, **kwargs) -> str:
        """
        获取登录地址
        """
        request: HttpRequest = self.request

        user = self.request.user
        if user.is_authenticated:
            # 如果已经登陆 跳转到首页 或者 next 地址
            return RedirectHelper.to_url(request, settings.QI_YU_SSO_INDEX_URI)

        # 没有登录
        # 登录成功的跳转地址
        login_next_url = RedirectHelper.to_url(request, settings.QI_YU_SSO_INDEX_URI)

        code_verifier = gen_code_verifier()

        request.session["code_verifier"] = code_verifier  # noqa

        # 跳转到登录地址
        sso_api = QiYuSSOSync()
        args = LoginArgs(
            server_uri=settings.QI_YU_LOGIN_URI,
            client_id=settings.QI_YU_SSO_CLIENT_ID,
            redirect_uri=f'{settings.QI_YU_SSO_REDIRECT_URI}?{urlencode({"next": login_next_url})}',
            state=secrets.token_hex(20),
            scope=settings.QI_YU_SSO_SCOPE,
            code_challenge=compute_code_challenge(code_verifier),
            code_challenge_method="S256",
        )
        return sso_api.get_login_url(args)
