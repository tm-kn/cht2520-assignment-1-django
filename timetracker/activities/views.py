from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from timetracker.activities.forms import ActivityForm
from timetracker.activities.models import Activity
from timetracker.sheets.models import Sheet


class SheetObjectMixin:

    @cached_property
    def sheet(self):
        return get_object_or_404(Sheet, pk=self.kwargs['sheet_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sheet'] = self.sheet
        return context


class NewActivityView(SheetObjectMixin, CreateView):
    form_class = ActivityForm
    template_name = 'activities/new.html'

    def get_success_url(self):
        return reverse_lazy(
            'activities:list', kwargs={'sheet_pk': self.sheet.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sheet': self.sheet})
        return kwargs


class ActivityListView(SheetObjectMixin, ListView):
    model = Activity

    def get_queryset(self):
        return self.model.objects.filter(project__sheet=self.sheet)
