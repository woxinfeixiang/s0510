# encoding: utf-8
# Created by wang on 2019/5/23

from .models import Course, Lesson, Video, CourseResource, BannerCourse
import xadmin


class CoureAdmin(object):
    list_display = ['name', 'desc',  'degree', 'learn_times', 'students']
    search_fields = ['name', 'degree']
    list_filter = ['name', 'students']
    ordering= ['-click_nums']
    readonly_fields = ['click_nums']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CoureAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)



