# encoding: utf-8
# Created by wang on 2019/7/22

from django import forms
import re
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

        # 手机号的正则表达式验证
        def clean_mobile(self):
            mobile = self.clean_mobile['mobile']
            REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
            p = re.compile(REGEX_MOBILE)
            if p.match(mobile):
                return mobile
            else:
                return forms.ValidationError(u"手机号码非法", code="mobile_invalid")
