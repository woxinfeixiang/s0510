# encoding: utf-8
# Created by wang on 2019/5/23
import xadmin


from xadmin import views
from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "我的小站"
    site_footer = "小站之地"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url']
    list_filter = ['title', 'url']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

# 将全局配置管理与view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)

# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSetting)
