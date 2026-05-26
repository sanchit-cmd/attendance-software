from django.contrib import admin
from .models import Attendance


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    fields = ("attendance_date", "is_present", "attendance_batch")
    ordering = ("-attendance_date",)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "attendance_date", "is_present", "attendance_batch")
    list_filter = ("is_present", "attendance_date", "attendance_batch")
    search_fields = ("enrollment__student__name", "enrollment__subject__name")
    date_hierarchy = "attendance_date"
    ordering = ("-attendance_date",)


admin.site.register(Attendance, AttendanceAdmin)
