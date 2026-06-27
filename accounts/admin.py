from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Hospital Details",
            {
                "fields": (
                    "role",
                    "specialization",
                    "phone",
                    "address",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Hospital Details",
            {
                "classes": ("wide",),
                "fields": (
                    "role",
                    "specialization",
                    "phone",
                    "address",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
    )