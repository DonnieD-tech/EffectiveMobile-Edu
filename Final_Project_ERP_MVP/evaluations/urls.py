from django.urls import path

from .views import EvaluationCreateView

urlpatterns = [
    path('task/<int:task_id>/user/<int:user_id>/add/',
         EvaluationCreateView.as_view(),
         name='evaluation_add'),
]
