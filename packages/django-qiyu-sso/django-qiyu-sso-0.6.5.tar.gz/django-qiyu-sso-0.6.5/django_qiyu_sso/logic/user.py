import logging
from typing import Type
from urllib.parse import urlencode

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django_qiyu_utils import RedirectHelper
from qiyu_sso.api import QiYuSSOSync
from qiyu_sso.forms import TokenArgs, UserInfoArgs
from qiyu_sso.resp import UserInfoResponse

from .. import settings

__all__ = ["UserLogic"]


class OAuthLoginForm(forms.Form):
    code = forms.CharField(max_length=256)
    state = forms.CharField(max_length=256)


class UserLogic(object):
    def __init__(self):
        self._log = logging.getLogger("django")

    def oauth_login(self, request: HttpRequest, form: OAuthLoginForm):
        """
        OAuth 授权登录
        :raises: ValidationError
        """
        code = form.cleaned_data["code"]
        state = form.cleaned_data["state"]
        self._log.info(f"oauth login {code=} {state=}")

        access_token = self._get_access_token(request, code)
        user_info = self._get_user_info(access_token=access_token)
        user = self._create_user_if_not_exists(user_info)

        # 用户登录 成功
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    def _create_user_if_not_exists(self, user_info: UserInfoResponse) -> AbstractUser:
        """
        如果不存在则创建用户
        否则 返回已经存在的用户
        """
        username = user_info.username
        # noinspection PyPep8Naming
        User: Type[AbstractUser] = get_user_model()
        user: AbstractUser = User.objects.filter(username=username).first()
        if user is not None:
            self._log.info(f"{user.username=} is exists")
            return user
        args = {"username": username}
        if user_info.is_staff:
            args["is_staff"] = True
        if user_info.is_admin:
            args["is_superuser"] = True
        if user_info.email is not None:
            args["email"] = user_info.email
        self._log.info(f"create user: {args=}")
        return User.objects.create_user(**args)

    def _get_user_info(self, access_token: str) -> UserInfoResponse:
        api = QiYuSSOSync()

        args = UserInfoArgs(
            server_uri=settings.QI_YU_USER_INFO_URI,
            access_token=access_token,
        )
        user_info = api.get_user_info(args)
        if user_info is None:
            self._log.error(f"fetch user info failed: {access_token=}")
            raise ValidationError(f"访问令牌: {access_token} 无效")
        return user_info

    def _get_access_token(self, request: HttpRequest, code: str) -> str:
        """
        使用 code 换取 访问令牌

        :raises: ValidationError
        :return str: 访问令牌
        """
        t = RedirectHelper.to_url(request, settings.QI_YU_SSO_INDEX_URI)

        code_verifier = request.session.get("code_verifier", None)  # noqa

        api = QiYuSSOSync()
        args = TokenArgs(
            # redirect_uri must be same as `/oauth/authorized/` request redirect_uri
            server_uri=settings.QI_YU_TOKEN_URI,
            redirect_uri=f'{settings.QI_YU_SSO_REDIRECT_URI}?{urlencode({"next": t})}',
            client_id=settings.QI_YU_SSO_CLIENT_ID,
            client_secret=settings.QI_YU_SSO_CLIENT_SECRET,
            code=code,
            code_verifier=code_verifier,
        )

        access_token = api.get_access_token(args)
        if access_token is None:
            self._log.error("fetch access token failed")
            raise ValidationError(f"授权码 {code=} 无效")
        return access_token.access_token
