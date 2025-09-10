from rest_framework import serializers

from evaluations.models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(
        source='task.title',
        read_only=True
    )
    user_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name',
        read_only=True
    )

    class Meta:
        model = Evaluation
        fields = [
            'id',
            'task',
            'task_title',
            'user',
            'user_name',
            'score',
            'created_by',
            'created_by_name',
            'comment',
            'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']


class EvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            'task',
            'user',
            'score',
            'comment'
        ]

    def validate(self, data):
        task = data['task']
        user = data['user']
        request_user = self.context['request'].user

        if task.status != task.Status.DONE:
            raise serializers.ValidationError(
                "Оценка может быть выставлена только выполненной задаче."
            )

        if Evaluation.objects.filter(
                task=task, user=user, created_by=request_user).exists():
            raise serializers.ValidationError(
                "Вы уже оценили этого пользователя за эту задачу."
            )

        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
