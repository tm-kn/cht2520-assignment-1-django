from django import forms

from timetracker.activities.models import Activity


class ActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        sheet = kwargs.pop('sheet')
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = (
            self.fields['project'].queryset.filter(sheet=sheet))

    class Meta:
        model = Activity
        fields = (
            'project',
            'activity',
            'description',
            'start_datetime',
            'end_datetime',
        )
