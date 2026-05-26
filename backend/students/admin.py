from django.contrib import admin
from django.forms import DateInput
from .models import Student
from enrollments.models import Enrollment


# Register your models here.
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    fields = ("subject", "status", "total_classes")
    readonly_fields = ("start_date", "end_date")
    autocomplete_fields = ("subject",)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__phone")
    autocomplete_fields = ("user",)
    inlines = [EnrollmentInline]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "date_of_birth":
            kwargs["widget"] = DateInput(attrs={"type": "date", "class": "vDateField"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


admin.site.register(Student, StudentAdmin)
