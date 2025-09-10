from django import forms

from meetings.models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = (
            'title',
            'description',
            'start_time',
            'end_time',
            'participants'
        )
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        participants = cleaned_data.get('participants')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "Встреча не может заканчиваться раньше, чем началась."
            )

        if start_time and end_time and participants:
            for user in participants:
                qs = user.meetings.exclude(id=self.instance.id)
                for meeting in qs:
                    if (start_time < meeting.end_time
                            and end_time > meeting.start_time):
                        raise forms.ValidationError(
                            f'У пользователя {user} уже есть встреча,'
                            f' пересекающаяся с этим временем'
                        )

        return cleaned_data
