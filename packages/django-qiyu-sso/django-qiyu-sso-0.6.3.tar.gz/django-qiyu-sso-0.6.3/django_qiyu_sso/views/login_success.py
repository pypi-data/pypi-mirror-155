from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import FormView
from django_qiyu_utils import RedirectHelper

from .. import settings
from ..logic import UserLogic

__all__ = ["LoginSuccessView"]


class OAuthLoginForm(forms.Form):
    code = forms.CharField(max_length=256)
    state = forms.CharField(max_length=256)


class LoginSuccessView(FormView):
    """
    OAuth2 登录成功之后跳转到这个页面
    """

    form_class = OAuthLoginForm

    template_name = "user/oauth_login_failure.html"

    def get(self, request, *args, **kwargs):
        # we do get method allow post method
        return self.post(request, *args, **kwargs)

    def form_valid(self, form: OAuthLoginForm):
        logic = UserLogic()
        try:
            logic.oauth_login(request=self.request, form=form)
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return super().form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        # 如果已经登陆 跳转到首页 或者 next 地址
        return RedirectHelper.to_url(self.request, settings.QI_YU_SSO_INDEX_URI)

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        if "data" not in kwargs:
            kwargs["data"] = self.request.GET
        return kwargs
