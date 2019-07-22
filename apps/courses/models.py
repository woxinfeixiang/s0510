# encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime
from organization.models import CourseOrg, Teacher
from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    DEGREE_CHOICES = (
        ("cj", u"初级"),
        ("zj", u"中级"),
        ("gj", u"高级")
    )
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u"教师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    desc = models.CharField(max_length=200, verbose_name=u"课程描述")
    #detail = UEditorField(verbose_name=u"课程详情", width=600, height=300, imagePath="courses/ueditor/", filePath="course/ueditor", default='')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name=u"难度")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    category = models.CharField(max_length=20, default=0, verbose_name=u"课程类别")
    you_need_know = models.CharField(default=u"一颗勤学的心是必备的", max_length=300, verbose_name=u"课程")
    teacher_tell = models.CharField(max_length=300, default=u"按时交作业,不然叫家长", verbose_name=u"老师告诉你")
    tag = models.CharField(max_length=15, verbose_name=u"课程标签", default=u"")
    image = models.ImageField(
        upload_to="course/%Y/%m",
        verbose_name=u"封面图",
        max_length=100
    )
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://blog.mtianyan.cn'>跳转</>")
    go_to.short_description = "跳转"

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.URLField(max_length=200, default="http://blog.mtianyan.cn/", verbose_name=u"访问地址")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}章节的视频 >> {1}'.format(self.lesson, self.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(
        upload_to="course/resource/%Y/%m",
        verbose_name=u"资源文件",
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '《{0}》课程的资源: {1}'.format(self.course, self.name)
