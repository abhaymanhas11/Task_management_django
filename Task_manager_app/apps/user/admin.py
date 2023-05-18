from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from django.contrib import admin
from apps.user.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from apps.utils.enum import UserType


class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (("User role"), {"fields": ("user_type",)}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "user_type",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    def save_model(self, request, obj, form, change):
        if obj.user_type == UserType.content_writer.name:
            obj.is_staff = False
            obj.is_superuser = False
            obj.is_active = True

        elif obj.user_type == UserType.editor.name:
            obj.is_staff = True
            obj.is_superuser = False
            obj.is_active = True

        else:
            obj.is_staff = True
            obj.is_superuser = True
            obj.is_active = True
        return super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)
