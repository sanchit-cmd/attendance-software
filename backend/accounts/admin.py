from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "role", "is_active")
    search_fields = ("phone", "name")
    list_filter = ("role", "is_active")

    fieldsets = (
        ("User Info", {"fields": ("phone", "name", "role")}),
        ("Password", {"fields": ("password",)}),
        ("Status", {"fields": ("is_active", "is_staff")}),
        # ("Permissions", {"fields": ("groups", "user_permissions")}),
    )


admin.site.register(User, UserAdmin)
