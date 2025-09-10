from datetime import date

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCalendarView:
    def test_calendar_view_requires_login(self, client):
        url = reverse("calendar")
        response = client.get(url)
        assert response.status_code == 302

    def test_calendar_view_renders_correct_template(
            self, client, manager, task, meeting_today):
        client.force_login(user=manager)
        url = reverse("calendar")
        response = client.get(url)
        assert response.status_code == 200
        assert "calendar_app/calendar_month.html" in [
            t.name for t in response.templates]

    def test_calendar_view_context_contains_tasks_and_meetings(
            self, client, manager, task, meeting_today):
        client.force_login(user=manager)
        url = reverse("calendar")
        response = client.get(url)
        context = response.context
        today_str = task.deadline.date().isoformat()
        assert today_str in context["events_by_day"]
        assert task in context["events_by_day"][today_str]
        assert meeting_today in context["events_by_day"][today_str]

    def test_calendar_view_filters_by_month(
            self, client, manager, task, meeting_other_month):
        client.force_login(user=manager)
        url = reverse("calendar") + \
            f"?year={date.today().year}&month={date.today().month}"
        response = client.get(url)
        context = response.context

        for day_events in context["events_by_day"].values():
            assert meeting_other_month not in day_events


@pytest.mark.django_db
class TestDayCalendarView:
    def test_day_calendar_view_requires_login(self, client, today):
        url = reverse(
            "day_calendar",
            args=[
                today.year,
                today.month,
                today.day])
        response = client.get(url)
        assert response.status_code == 302

    def test_day_calendar_view_renders_correct_template(
            self, client, manager, task, meeting_today):
        client.force_login(user=manager)
        url = reverse(
            "day_calendar",
            args=[
                task.deadline.year,
                task.deadline.month,
                task.deadline.day])
        response = client.get(url)
        assert response.status_code == 200
        assert "calendar_app/day_calendar.html" in [
            t.name for t in response.templates]

    def test_day_calendar_view_context_contains_correct_tasks_and_meetings(
            self, client, manager, task, meeting_today):
        client.force_login(user=manager)
        url = reverse(
            "day_calendar",
            args=[
                task.deadline.year,
                task.deadline.month,
                task.deadline.day])
        response = client.get(url)
        context = response.context
        assert task in context["tasks"]
        assert meeting_today in context["meetings"]

    def test_day_calendar_view_filters_by_day(
            self, client, manager, task, meeting_other_month):
        client.force_login(user=manager)
        url = reverse(
            "day_calendar",
            args=[
                task.deadline.year,
                task.deadline.month,
                task.deadline.day])
        response = client.get(url)
        context = response.context
        assert meeting_other_month not in context["meetings"]
