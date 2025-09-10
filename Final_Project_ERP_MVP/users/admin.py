from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "team",
        "is_active",
        "is_staff"
    )
    list_filter = (
        "role",
        "team",
        "is_active",
        "is_staff"
    )
    search_fields = (
        "email",
        "first_name",
        "last_name"
    )
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные",
         {"fields": (
             "first_name",
             "last_name",
             "role", "team"
         )
         }
         ),
        ("Права доступа",
         {"fields": (
             "is_active",
             "is_staff",
             "is_superuser",
             "groups",
             "user_permissions"
         )
         }
         ),
        ("Даты",
         {"fields": ("last_login",)
          }
         ),
    )
    add_fieldsets = (
        (None,
         {
             "classes": ("wide",),
             "fields": (
                 "email",
                 "first_name",
                 "last_name",
                 "password1",
                 "password2",
                 "role",
                 "team",
                 "is_active",
                 "is_staff"
             )
         }
         ),
    )
