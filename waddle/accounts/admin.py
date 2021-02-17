from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "email", "mobile", "is_active"]
    list_filter = ["is_active"]
    fieldsets = (
        ("Personal info", {"fields": ("name", "email", "mobile", "password")}),
        (
            "Permissions", 
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_staff",
                    "is_superuser"
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()
        super().save_model(request, obj, form, change)
