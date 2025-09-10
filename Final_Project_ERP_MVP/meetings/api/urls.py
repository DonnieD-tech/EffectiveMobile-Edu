from django.urls import path

from meetings.api.views import MeetingDetailView, MeetingListCreateView

urlpatterns = [
    path("", MeetingListCreateView.as_view(),
         name="meeting_list_create"),
    path("<int:pk>/", MeetingDetailView.as_view(),
         name="meeting_detail_delete"),
]
