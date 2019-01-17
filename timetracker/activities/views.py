from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import View
from django.views.generic.detail import (DetailView, SingleObjectMixin,
                                         SingleObjectTemplateResponseMixin)
from django.views.generic.edit import BaseUpdateView, CreateView, DeleteView
from django.views.generic.list import ListView

from timetracker.activities.forms import ActivityForm, ActivityFilterForm
from timetracker.activities.models import Activity


class ActivityQuerySetMixin:
    model = Activity

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ActivitySingleObjectMixin(ActivityQuerySetMixin, SingleObjectMixin):
    pass


class ActivityCreateView(LoginRequiredMixin, CreateView):
    form_class = ActivityForm
    template_name = 'activities/activity_create.html'
    success_url = reverse_lazy('activities:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ActivityListView(LoginRequiredMixin, ActivityQuerySetMixin, ListView):
    def get_queryset(self):
        start_of_range = self.get_start_of_range()
        end_of_range = self.get_end_of_range()
        if start_of_range > end_of_range:
            start_of_range, end_of_range = end_of_range, start_of_range
        start_of_range = timezone.datetime.combine(
            start_of_range, timezone.datetime.min.time())
        end_of_range = timezone.datetime.combine(end_of_range, timezone.datetime.max.time())
        return super().get_queryset().filter(
            start_datetime__gte=start_of_range,
            start_datetime__lte=end_of_range)

    def get_start_of_range(self):
        start_date = None
        try:
            start_date = parse_date(self.request.GET['start_date'])
        except KeyError:
            pass
        if start_date is None:
            start_date = timezone.now().date() - timezone.timedelta(days=7)
        return start_date

    def get_end_of_range(self):
        end_date = None
        try:
            end_date = parse_date(self.request.GET['end_date'])
        except KeyError:
            pass
        if end_date is None:
            end_date = timezone.now().date()
        return end_date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form_data = self.request.GET.copy()
        filter_form_data.setdefault('start_date', self.get_start_of_range())
        filter_form_data.setdefault('end_date', self.get_end_of_range())
        context['filter_form'] = ActivityFilterForm(filter_form_data)
        return context


class ActivityDetailView(LoginRequiredMixin, ActivitySingleObjectMixin,
                         DetailView):
    pass


class ActivityUpdateView(LoginRequiredMixin, ActivitySingleObjectMixin,
                         SingleObjectTemplateResponseMixin, BaseUpdateView):
    form_class = ActivityForm
    template_name = 'activities/activity_update.html'


class ActivityStopView(ActivitySingleObjectMixin, View):
    def post(self, *args, **kwargs):
        obj = self.get_object()
        obj.stop()
        return redirect('activities:list')


class ActivityDeleteView(ActivitySingleObjectMixin, DeleteView):
    success_url = reverse_lazy('activities:list')
