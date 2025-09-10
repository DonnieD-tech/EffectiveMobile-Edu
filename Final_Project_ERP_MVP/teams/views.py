from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from tasks.models import Task
from teams.forms import AddMemberForm, JoinTeamForm
from teams.models import Team
from users.models import User


@login_required
def join_team(request):
    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['invite_code']
            try:
                team = Team.objects.get(invite_code=code)
                request.user.team = team
                request.user.role = User.Role.USER
                request.user.save()
                messages.success(
                    request,
                    f'Вы успешно присоединились'
                    f' к команде: {team.name}'
                )
                return redirect('team_detail',
                                team.id)
            except Team.DoesNotExist:
                messages.error(
                    request,
                    'Неверный код приглашения'
                )
    else:
        form = JoinTeamForm()

    return render(
        request,
        'teams/join_team.html',
        {'form': form}
    )


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = ["name"]
    template_name = "teams/team_create.html"
    success_url = reverse_lazy("team_detail")

    def form_valid(self, form):
        team = form.save(commit=False)
        team.admin = self.request.user
        team.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'team_detail',
            kwargs={'pk': self.object.pk}
        )


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team_detail.html"
    context_object_name = "team"

    def get(self, request, *args, **kwargs):
        team = self.get_object()

        if (not request.user.is_superuser
                and request.user.team != team):
            messages.warning(
                request,
                'Вы не состоите в этой команде'
            )
            return redirect('join_team')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context["tasks"] = (
            Task.objects.filter(
                team=self.object
            ).select_related('assignee')
        )
        context["members"] = team.members.all()
        return context


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    fields = ["name"]
    template_name = "teams/team_update.html"

    def test_func(self):
        team = self.get_object()
        user = self.request.user
        return (
            user.is_superuser
            or team.admin == user
            or (user.team == team and user.role == User.Role.ADMIN_TEAM)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "add_member_form" not in context:
            context["add_member_form"] = AddMemberForm()
        context["members"] = self.object.members.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "add_member" in request.POST:
            form = AddMemberForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data["user"]

                if user.team and user.team != self.object:
                    user.team = None

                user.team = self.object
                user.role = User.Role.USER
                user.save()

                messages.success(
                    request,
                    f"Пользователь {user.email}"
                    f" добавлен в команду {self.object.name}"
                )
                return redirect("team_edit", pk=self.object.pk)
            else:
                return self.render_to_response(
                    self.get_context_data(add_member_form=form))

        if "remove_member" in request.POST:
            user_id = request.POST.get("remove_member")
            user = User.objects.get(pk=user_id)
            if user == self.object.admin:
                messages.error(
                    request,
                    "Нельзя исключить администратора команды"
                )
            elif user.team == self.object:
                user.team = None
                user.role = User.Role.USER
                user.save()
                messages.success(
                    request,
                    f"Пользователь {user.email}"
                    f" удалён из команды"
                )
            return redirect("team_edit", pk=self.object.pk)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('team_detail', args=[self.object.id])


@login_required
def team_manage_roles(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if (request.user != team.admin and
            not request.user.is_superuser):
        raise PermissionDenied(
            'Вы не являетесь админом этой команды'
        )

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        member = get_object_or_404(User, id=user_id, team=team)

        if member == request.user:
            messages.error(
                request,
                'Вы не можете изменить свою роль'
            )
        else:
            member.role = new_role
            member.save()
            messages.success(
                request,
                f'Роль пользователя {member.first_name}'
                f' {member.last_name} изменена на'
                f' {member.get_role_display()}.'
            )

        return redirect('team_manage_roles', team.id)

    members = team.members.all()
    return render(
        request,
        'teams/team_manage_roles.html',
        {
            'team': team,
            'members': members,
            'roles': User.Role.choices,
        }
    )
