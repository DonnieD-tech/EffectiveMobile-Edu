from django.contrib import admin

from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "invite_code",
        "admin"
    )
    search_fields = (
        "name",
        "invite_code"
    )
