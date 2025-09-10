import pytest

from evaluations.forms import EvaluationForm


@pytest.mark.django_db
class TestEvaluationForm:
    def test_form_valid_data(self):
        form = EvaluationForm(data={
            "score": 4,
            "comment": "Хорошая работа"
        })
        assert form.is_valid()

    def test_form_valid_without_comment(self):
        form = EvaluationForm(data={"score": 5})
        assert form.is_valid()
        assert form.cleaned_data["comment"] == ""

    def test_form_invalid_without_score(self):
        form = EvaluationForm(data={"comment": "Без оценки"})
        assert not form.is_valid()
        assert "score" in form.errors

    def test_form_invalid_score_too_low(self):
        form = EvaluationForm(data={"score": 0})
        assert not form.is_valid()
        assert "score" in form.errors

    def test_form_invalid_score_too_high(self):
        form = EvaluationForm(data={"score": 6})
        assert not form.is_valid()
        assert "score" in form.errors

    def test_form_labels(self):
        form = EvaluationForm()
        assert form.fields["score"].label == "Оценка (1-5)"
        assert form.fields["comment"].label == "Комментарий"
