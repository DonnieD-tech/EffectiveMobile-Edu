from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from evaluations.forms import EvaluationForm
from tasks.forms import TaskCommentForm, TaskForm
from tasks.models import Task
from users.models import User


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(
            team=self.request.user.team
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        task = self.get_object()
        evaluation = task.evaluations.order_by('-created_at')

        context['can_edit'] = user.role in (
            User.Role.MANAGER,
            User.Role.ADMIN_TEAM
        )
        context['can_change_status'] = (
            user == task.assignee
            or user.role in
            (
                User.Role.MANAGER,
                User.Role.ADMIN_TEAM
            )
        )
        context['evaluations'] = evaluation
        context['form'] = TaskCommentForm()

        context['can_add_evaluation'] = (
            task.status == Task.Status.DONE
            and not evaluation.filter
            (user=user).exists()
        )
        context['evaluation_form'] = EvaluationForm()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        team = self.request.user.team
        if not team:
            form.add_error(
                None,
                'Вы не состоите в команде,'
                ' задача не может быть создана.'
            )
            return self.form_invalid(form)

        form.instance.created_by = self.request.user
        form.instance.team = team

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'team_detail',
            kwargs={'pk': self.request.user.team.id}
        )


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return (Task.objects.filter(
            team=self.request.user.team
        ).select_related('assignee')
        )


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'

    def get_queryset(self):
        return Task.objects.filter(
            team=self.request.user.team
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.role not in [
                User.Role.MANAGER, User.Role.ADMIN_TEAM]:
            form.add_error(
                None,
                "У вас нет прав на редактирование задачи"
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "team_detail",
            kwargs={"pk": self.request.user.team.id}
        )


class TaskCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = Task.objects.get(
            pk=pk,
            team=request.user.team
        )
        form = TaskCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

        return redirect('task_detail', pk=task.id)


class TaskChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(
            Task,
            id=pk,
            team=request.user.team
        )
        new_status = request.POST.get("status")

        if not (
            request.user == task.assignee
            or request.user.role in
            [User.Role.MANAGER, User.Role.ADMIN_TEAM]
        ):
            raise PermissionDenied(
                "У вас нет прав для изменения статуса задачи"
            )

        valid_statuses = [choice[0] for choice in Task.Status.choices]

        if new_status not in valid_statuses:
            messages.error(request, "Некорректный статус")
            return redirect("task_detail", pk=task.id)

        task.status = new_status
        task.save()
        messages.success(
            request,
            f"Статус задачи изменён на"
            f" «{task.get_status_display()}»."
        )

        return redirect("task_detail", pk=task.id)


class TeamTaskListView(LoginRequiredMixin, ListView, CreateView):
    model = Task
    template_name = 'tasks/team_tasks.html'
    context_object_name = 'tasks'
    form_class = TaskForm

    def get_queryset(self):
        return (Task.objects.filter(
            team=self.request.user.team
        ).select_related('assignee')
        )

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.team = self.request.user.team

        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if (request.user.role not in
                (request.user.Role.MANAGER,
                 request.user.Role.ADMIN_TEAM)):
            raise PermissionDenied(
                "Вы не можете удалять эту задачу."
            )
        task.delete()

        return redirect('task_list')
