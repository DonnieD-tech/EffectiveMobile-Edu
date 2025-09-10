from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

from evaluations.forms import EvaluationForm
from evaluations.models import Evaluation
from tasks.models import Task
from users.models import User


class EvaluationCreateView(LoginRequiredMixin, CreateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'evaluations/evaluation_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role not in (User.Role.MANAGER, User.Role.ADMIN_TEAM):
            raise PermissionDenied('Вы не можете ставить оценки')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)

        context['task'] = task
        context['target_user'] = user

        return context

    def form_valid(self, form):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        user = get_object_or_404(User, id=self.kwargs['user_id'],
                                 team=self.request.user.team)

        form.instance.task = task
        form.instance.user = user
        form.instance.created_by = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task_detail',
                            kwargs={'pk': self.kwargs['task_id']}
                            )
