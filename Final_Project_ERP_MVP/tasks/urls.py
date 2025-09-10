from django.urls import path

from .views import (
    TaskChangeStatusView,
    TaskCommentCreateView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns = [
    path("create/", TaskCreateView.as_view(),
         name="task_create"),
    path("list/", TaskListView.as_view(),
         name="task_list"),
    path("<int:pk>/", TaskDetailView.as_view(),
         name="task_detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(),
         name="task_update"),
    path('<int:pk>/comment/', TaskCommentCreateView.as_view(),
         name="task_comment_create"),
    path("<int:pk>/change_status/", TaskChangeStatusView.as_view(),
         name="task_change_status"),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(),
         name='task_delete'),
]
