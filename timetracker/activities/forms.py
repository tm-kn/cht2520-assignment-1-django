from django import forms
from django.utils.translation import ugettext_lazy as _

from timetracker.activities.models import Activity
from timetracker.utils.widgets import DatePickerWidget, DateTimePickerWidget


class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        activity = super().save(commit=False)
        if self.user is not None:
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


class ActivityFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False, widget=DatePickerWidget(), label=_('Start date'))
    end_date = forms.DateField(
        required=False, widget=DatePickerWidget(), label=_('End date'))
    search_query = forms.CharField(required=False, label=_('Search query'))
