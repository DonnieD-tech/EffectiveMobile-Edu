from django.urls import path

from teams.api.views import TeamCreateView, TeamDetailView, TeamJoinView

urlpatterns = [
    path("", TeamCreateView.as_view(),
         name="team_create"),
    path("<int:pk>/", TeamDetailView.as_view(),
         name="team_detail"),
    path("join/", TeamJoinView.as_view(),
         name="team_join"),
]
