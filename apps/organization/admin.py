from django.contrib import admin

# Register your models here.
from .models import CourseOrg


class CourseOrgAdmin(admin.ModelAdmin):
    pass


admin.site.register(CourseOrg, CourseOrgAdmin)
