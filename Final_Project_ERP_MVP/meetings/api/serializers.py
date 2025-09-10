from rest_framework import serializers

from meetings.models import Meeting
from users.models import User


class MeetingSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Meeting
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "created_by",
            "participants"
        ]
        read_only_fields = ["id", "created_by"]

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        participants = data.get("participants", [])

        if start_time >= end_time:
            raise serializers.ValidationError(
                "Встреча не может заканчиваться раньше,"
                " чем началась."
            )

        for user in participants:
            overlapping = Meeting.objects.filter(
                participants=user,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if self.instance:
                overlapping = overlapping.exclude(
                    pk=self.instance.pk
                )
            if overlapping.exists():
                raise serializers.ValidationError(
                    f"У пользователя {user.email}"
                    f" уже есть встреча в это время."
                )
        return data
