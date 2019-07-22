# encoding: utf-8
"""s0510 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve


import xadmin
from s0510.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ModifyPwdView, ResetView, \
    IndexView
from organization.views import OrgView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # url('^$', IndexView.as_view(), name="index"),


    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    # 忘记密码
    url(r'^forget/', ForgetView.as_view(), name="forget_pwd"),
    # 重置密码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    # 修改密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    # 激活账户
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 课程机构
    url(r'^org-list/$', OrgView.as_view(), name="modify_pwd"),
    #url(r'^org/', include('organization.urls', name="org")),
    # 图片路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT }),
]
