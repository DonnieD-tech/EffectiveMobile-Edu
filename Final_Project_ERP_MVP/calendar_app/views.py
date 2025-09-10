import calendar
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from meetings.models import Meeting
from tasks.models import Task


class CalendarView(LoginRequiredMixin, View):
    template_name = "calendar_app/calendar_month.html"

    def get(self, request, *args, **kwargs):
        year = int(request.GET.get("year", date.today().year))
        month = int(request.GET.get("month", date.today().month))

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(year, month)

        tasks = Task.objects.filter(
            deadline__year=year,
            deadline__month=month
        )
        meetings = Meeting.objects.filter(
            start_time__year=year,
            start_time__month=month
        )

        events_by_day = {}

        for task in tasks:
            (events_by_day.setdefault(
                task.deadline.date().isoformat(), []).append(task)
             )

        for meeting in meetings:
            (events_by_day.setdefault(
                meeting.start_time.date().isoformat(), []).append(meeting)
             )

        if month == 1:
            prev_month = date(year - 1, 12, 1)
        else:
            prev_month = date(year, month - 1, 1)

        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)

        MONTHS_RU = {
            1: "Январь",
            2: "Февраль",
            3: "Март",
            4: "Апрель",
            5: "Май",
            6: "Июнь",
            7: "Июль",
            8: "Август",
            9: "Сентябрь",
            10: "Октябрь",
            11: "Ноябрь",
            12: "Декабрь",
        }

        context = {
            "calendar": month_days,
            "events_by_day": events_by_day,
            "current_year": year,
            "current_month": month,
            "current_month_name": MONTHS_RU[month],
            "prev_month": {"year": prev_month.year,
                           "month": prev_month.month
                           },
            "next_month": {"year": next_month.year,
                           "month": next_month.month
                           },
        }

        return render(request, self.template_name, context)


class DayCalendarView(LoginRequiredMixin, View):
    template_name = "calendar_app/day_calendar.html"

    def get(self, request, year, month, day, *args, **kwargs):
        current_day = date(
            year=int(year),
            month=int(month),
            day=int(day)
        )

        tasks = Task.objects.filter(
            deadline__date=current_day
        )

        meetings = Meeting.objects.filter(
            start_time__date=current_day
        )

        context = {
            "current_day": current_day,
            "tasks": tasks,
            "meetings": meetings,
        }

        return render(request, self.template_name, context)
