from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from evaluations.models import Evaluation
from teams.models import Team
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs

        if not self.request.user.team:
            return qs.filter(pk=self.request.user.pk)

        return qs.filter(team=self.request.user.team)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        if self.request.user.is_superuser:
            context["teams"] = Team.objects.all()

        evaluations = Evaluation.objects.filter(
            task__assignee=user
        )

        context["recent_evaluations"] = evaluations.order_by("-created_at")[:5]
        context["evaluation_count"] = evaluations.count()
        avg_score = evaluations.aggregate(avg=Avg("score"))["avg"]
        context["avg_score"] = round(avg_score, 2) if avg_score else 0
        return context


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy('user_detail')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)

        team_code = form.cleaned_data.get('team_code')
        if team_code:
            team = Team.objects.filter(
                invite_code=team_code
            ).first()
            if team:
                self.request.user.team = team
                self.request.user.save()
        return response


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user
