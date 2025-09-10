from rest_framework import serializers

from teams.models import Team
from users.models import User


class TeamSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'invite_code',
            'admin',
            'members'
        )

    def get_members(self, obj):
        return [
            {
                'id': user.id,
                'email': user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            }
            for user in User.objects.filter(team=obj)
        ]


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]

    def create(self, validated_data):
        user = self.context["request"].user
        team = Team.objects.create(admin=user,
                                   **validated_data
                                   )
        user.team = team
        user.save()
        return team


class TeamJoinSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=12)

    def validate_invite_code(self, value):
        try:
            return Team.objects.get(invite_code=value)
        except Team.DoesNotExist:
            raise serializers.ValidationError(
                "Неверный код приглашения"
            )

    def create(self, validated_data):
        team = validated_data["invite_code"]
        user = self.context["request"].user
        user.team = team
        user.save()
        return team
