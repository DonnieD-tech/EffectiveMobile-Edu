from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView, DeleteView, ListView
from rest_framework.reverse import reverse_lazy

from meetings.forms import MeetingForm
from meetings.models import Meeting


class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/meeting_form.html'
    success_url = reverse_lazy('meeting_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'meetings/meeting_list.html'
    context_object_name = 'meetings'

    def get_queryset(self):
        return (Meeting.objects.filter(
            Q(created_by=self.request.user) |
            Q(participants=self.request.user))
            .distinct().order_by('start_time')
        )


class MeetingCancelView(LoginRequiredMixin, DeleteView):
    model = Meeting
    template_name = 'meetings/meeting_confirm_cancel.html'
    context_object_name = 'meeting'
    success_url = reverse_lazy('meeting_list')

    def get_queryset(self):
        return Meeting.objects.filter(
            created_by=self.request.user
        )
