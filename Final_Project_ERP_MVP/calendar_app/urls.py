from django.urls import path

from calendar_app.views import CalendarView, DayCalendarView

urlpatterns = [
    path("calendar/", CalendarView.as_view(),
         name="calendar"),
    path("calendar/<int:year>/<int:month>/<int:day>/",
         DayCalendarView.as_view(),
         name="day_calendar"),
]
