from django import forms

from evaluations.models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ('score', 'comment')
        labels = {
            'score': 'Оценка (1-5)',
            'comment': 'Комментарий'
        }
