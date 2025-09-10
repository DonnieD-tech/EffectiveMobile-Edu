from django.urls import path

from meetings.views import (
    MeetingCancelView,
    MeetingCreateView,
    MeetingListView,
)

urlpatterns = [
    path('list/', MeetingListView.as_view(),
         name='meeting_list'),
    path('create/', MeetingCreateView.as_view(),
         name='meeting_create'),
    path('<int:pk>/cancel/', MeetingCancelView.as_view(),
         name='meeting_cancel'),
]
