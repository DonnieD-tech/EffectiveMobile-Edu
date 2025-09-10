from django.urls import path

from .views import (
    EvaluationByTaskView,
    EvaluationListCreateView,
    UserAverageEvaluationView,
)

urlpatterns = [
    path('', EvaluationListCreateView.as_view(),
         name='evaluation_list_create'),
    path('task/<int:task_id>/', EvaluationByTaskView.as_view(),
         name='evaluation_by_task'),
    path('user/<int:user_id>/average/', UserAverageEvaluationView.as_view(),
         name='user_average_evaluation'),
]
