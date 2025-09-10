from rest_framework import serializers

from tasks.models import Task, TaskComment


class TaskCommentSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()

    class Meta:
        model = TaskComment
        fields = [
            "id",
            "author",
            "author_full_name",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "author", "created_at"]

    def get_author_full_name(self, obj):
        if obj.author.first_name or obj.author.last_name:
            return (f"{obj.author.first_name}"
                    f" {obj.author.last_name}").strip()
        return obj.author.email


class TaskSerializer(serializers.ModelSerializer):
    assignee_full_name = serializers.SerializerMethodField()
    created_by_full_name = serializers.SerializerMethodField()
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "assignee",
            "assignee_full_name",
            "team",
            "created_by",
            "created_by_full_name",
            "comments",
        ]
        read_only_fields = ["id", "created_by", "comments"]

    def get_assignee_full_name(self, obj):
        if obj.assignee:
            if obj.assignee.first_name or obj.assignee.last_name:
                return (f"{obj.assignee.first_name}"
                        f" {obj.assignee.last_name}").strip()
            return obj.assignee.email

        return None

    def get_created_by_full_name(self, obj):
        if obj.created_by.first_name or obj.created_by.last_name:
            return (f"{obj.created_by.first_name}"
                    f" {obj.created_by.last_name}").strip()

        return obj.created_by.email


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "assignee",
            "team"
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user

        return super().create(validated_data)


class TaskCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ["id", "content"]
