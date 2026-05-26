from django.contrib import admin
from .models import Enrollment
from attendance.admin import AttendanceInline

# Register your models here.


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "status", "start_date", "end_date")
    list_filter = ("status", "subject__name")
    search_fields = (
        "student__name",
        "subject__name",
        "student__user__phone",
        "student__user__name",
    )
    autocomplete_fields = ("student", "subject")
    inlines = [AttendanceInline]
    readonly_fields = ("start_date", "end_date", "created_at")


admin.site.register(Enrollment, EnrollmentAdmin)
