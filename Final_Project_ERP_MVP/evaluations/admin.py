from django.contrib import admin

from evaluations.models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "user",
        "score",
        "created_by",
        "created_at"
    )
    list_filter = ("score", "created_at")
    search_fields = (
        "task__title",
        "user__email",
        "comment"
    )
    ordering = ("-created_at",)
