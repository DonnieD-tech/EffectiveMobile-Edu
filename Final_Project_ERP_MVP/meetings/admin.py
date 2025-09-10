from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "created_by")
    list_filter = ("start_time", "end_time")
    search_fields = ("title", "description")
    filter_horizontal = ("participants",)
