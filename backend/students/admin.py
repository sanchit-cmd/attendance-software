from django.contrib import admin
from django.forms import DateInput
from .models import Student


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__phone")
    autocomplete_fields = ("user",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "date_of_birth":
            kwargs["widget"] = DateInput(attrs={"type": "date", "class": "vDateField"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


admin.site.register(Student, StudentAdmin)
