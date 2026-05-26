from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "role", "is_active")
    search_fields = ("phone", "name")
    list_filter = ("role", "is_active")

    fieldsets = (
        ("User Info", {"fields": ("phone", "name", "role")}),
        ("Password", {"fields": ("password",)}),
        ("Status", {"fields": ("is_active", "is_staff")}),
    )

    def save_model(self, request, obj, form, change):
        # New user
        if not change:
            obj.set_password(obj.password)

        # Existing user password changed
        elif "password" in form.changed_data:
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)
