from django import forms

from timetracker.activities.models import Activity
from timetracker.utils.widgets import DateTimePickerWidget


class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        activity = super().save(commit=False)
        activity.user = self.user
        if commit:
            activity.save()
        return activity

    class Meta:
        model = Activity
        fields = (
            'project',
            'activity',
            'description',
            'start_datetime',
            'end_datetime',
        )
        widgets = {
	    'start_datetime': DateTimePickerWidget(),
	    'end_datetime': DateTimePickerWidget(),
	}
