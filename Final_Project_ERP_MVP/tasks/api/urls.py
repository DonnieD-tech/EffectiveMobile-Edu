from django.urls import path

from tasks.api.views import (
    TaskCommentDetailView,
    TaskCommentListCreateView,
    TaskDetailView,
    TaskListCreateView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(),
         name="task_list_create"),
    path("<int:pk>/", TaskDetailView.as_view(),
         name="task_detail"),
    path("<int:task_id>/comments/", TaskCommentListCreateView.as_view(),
         name="task_comments"),
    path("<int:task_id>/comments/<int:pk>/", TaskCommentDetailView.as_view(),
         name="task_comment_detail"),
]
