# encoding: utf-8
# Created by wang on 2019/5/28
from django import forms
# 引入验证码field
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 激活用验证码激活
class ActiveForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


# 验证form && 注册表单form
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


# 忘记密码实现
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


# 重置密码
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
