# encoding: utf-8
# Created by wang on 2019/5/30
from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail, EmailMessage
from s0510.settings import EMAIL_FROM
from django.template import loader


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_regiter_email(email, send_type="regiter"):

    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "我的小站,发送激活链接"
        email_body = loader.render_to_string("email_register.html",
                                             {
                                                 "active_code":code
                                             })
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "我的小站  找回密码链接"
        email_body = loader.render_to_string("email_forget.html",
                                             {
                                                 "active_code": code
                                             })
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
    elif send_type == "update_email":
        email_title = "我的小站 修改邮箱验证码"
        email_body = loader.render_to_string("email_update_email.html",
                                             {
                                                 "active_code": code
                                             })
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()













