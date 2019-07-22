# encoding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# 基于类实现需要继承的view
from django.views.generic.base import View

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm
# 进行密码加密
from django.contrib.auth.hashers import make_password
# 发送邮件
from utils.email_send import send_regiter_email


# Create your views here.

# 视频6-3


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 视频6-5
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg":"用户名或密码错误"})
#     elif request.method == "GET":
#         return render(request, "login.html", {})


# 注册功能的view-- 视频6-9
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在"})
            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为false
            user_profile.is_active = False

            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # # 注册功能的view-- 视频6-10
            # # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册小站"
            user_message.save()

            # 发送注册邮件
            send_regiter_email(user_name, "register")
            return render(request, 'login.html', )
        else:
            return render(request, "register.html", {"register_form": register_form})


# 处理忘记密码
class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm
        return render(request, "forgetpwd.html", {"forget_form": forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_regiter_email(email, "forget")
            return render(request, "login.html", {"msg": "重置密码已发送，请查收"})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form = ActiveForm
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "forgetpwd.html", {"msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})


class ModifyPwdView(View):
    def post(self, request):
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html", {"msg": "密码修改成功, 请登录"})
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modiypwd_form": modiypwd_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱记录
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, "login.html", )
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效", "active_form": active_form})

# # 用户个人信息
# class UserInfoView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'next'
#
#     def get(self, request):
#         return render(request, "")


# 2019年6月4日
class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')[:5]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "all_banner": all_banner,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })

