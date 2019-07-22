# encoding: utf-8
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
# 处理分页
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# 课程机构
from courses.models import Course
from operation.models import UserFavorite
from .models import CourseOrg, CityDict, Teacher
from organization.forms import UserAskForm
from django.http import HttpResponse
# Create your views here.


class OrgView(View):
    def get(self,request):
        #return render(request, "org-list.html", {})
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        search_keywords = request.GET.get("keywords", '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                       Q(address__icontains=search_keywords))
        all_city = CityDict.objects.all()
        city_id = request.GET.get('city', "")
        # 城市
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        category = request.GET.get('ct', "")
        # 类别筛选
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "student":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_city": all_city,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "search_keywords": search_keywords,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误，请检查"}', content_type='application/json')



