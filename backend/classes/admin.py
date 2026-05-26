from django.contrib import admin
from django.db.models import Q
from .models import Subject, Teacher
from accounts.models import UserRole

# Register your models here.


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "user")
    search_fields = ("name", "user__phone", "subject__name")
    autocomplete_fields = ("user", "subject")


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)
