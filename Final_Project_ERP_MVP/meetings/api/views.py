from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from meetings.models import Meeting

from .serializers import MeetingSerializer


class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (Meeting.objects.filter(participants=user)
                | Meeting.objects.filter(created_by=user)
                )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MeetingDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Meeting.objects.all()

    def perform_destroy(self, instance):
        user = self.request.user
        if (user != instance.created_by and
                user.role != user.Role.MANAGER):
            raise PermissionDenied(
                "Удалять встречу может только"
                " создатель или менеджер.")
        instance.delete()
