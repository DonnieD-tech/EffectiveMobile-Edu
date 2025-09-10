from django.urls import path

from tasks.views import TeamTaskListView
from teams import views

urlpatterns = [
    path('join/', views.join_team,
         name='join_team'),
    path('create/', views.TeamCreateView.as_view(),
         name='team_create'),
    path('<int:pk>/detail/', views.TeamDetailView.as_view(),
         name='team_detail'),
    path('<int:pk>/detail/edit/', views.TeamUpdateView.as_view(),
         name='team_edit'),
    path('<int:team_id>/detail/roles/', views.team_manage_roles,
         name='team_manage_roles'),
    path("<int:pk>/tasks/", TeamTaskListView.as_view(),
         name="team_tasks"),
]
