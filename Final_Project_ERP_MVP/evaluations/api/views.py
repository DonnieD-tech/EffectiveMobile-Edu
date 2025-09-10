from django.db.models import Avg
from django.utils.dateparse import parse_date
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from ..models import Evaluation
from .serializers import EvaluationCreateSerializer, EvaluationSerializer


class EvaluationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EvaluationCreateSerializer
        return EvaluationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role in [user.Role.MANAGER, user.Role.ADMIN_TEAM]:
            return Evaluation.objects.all()
        return Evaluation.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in [user.Role.MANAGER, user.Role.ADMIN_TEAM]:
            raise PermissionDenied(
                "Только менеджер может выставлять оценки."
            )
        serializer.save()


class EvaluationByTaskView(generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Evaluation.objects.filter(task_id=task_id)


class UserAverageEvaluationView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        start_param = request.GET.get("start")
        end_param = request.GET.get("end")

        start_date = parse_date(start_param) if start_param else None
        end_date = parse_date(end_param) if end_param else None

        qs = Evaluation.objects.filter(user_id=user_id)

        if start_date:
            qs = qs.filter(
                created_at__date__gte=start_date
            )
        if end_date:
            qs = qs.filter(
                created_at__date__lte=end_date
            )

        avg = qs.aggregate(avg_score=Avg('score'))['avg_score']
        return Response({'user_id': user_id,
                         'average_score': avg}
                        )
