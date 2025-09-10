from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from teams.api.serializers import (
    TeamCreateSerializer,
    TeamJoinSerializer,
    TeamSerializer,
)
from teams.models import Team


class TeamCreateView(generics.CreateAPIView):
    serializer_class = TeamCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamDetailView(generics.RetrieveAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class TeamJoinView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TeamJoinSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        return Response(TeamSerializer(team).data)
