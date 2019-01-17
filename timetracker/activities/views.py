from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
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
        start_of_range = self.filter_form.cleaned_data.get('start_date')
        end_of_range = self.filter_form.cleaned_data.get('end_date')
        qs = super().get_queryset()
        if start_of_range and end_of_range:
            if start_of_range > end_of_range:
                start_of_range, end_of_range = end_of_range, start_of_range
            start_of_range = timezone.datetime.combine(
                start_of_range, timezone.datetime.min.time())
            end_of_range = timezone.datetime.combine(end_of_range,
                                                    timezone.datetime.max.time())
            qs &= super().get_queryset().filter(
                start_datetime__gte=start_of_range,
                start_datetime__lte=end_of_range)

        search_query = self.filter_form.cleaned_data['search_query']
        if search_query:
            # Search query using Postgres full-text search.
            qs &= super().get_queryset().annotate(
                search=SearchVector('activity', 'project', 'description'),
            ).filter(search=search_query)
        return qs

    def get_filter_form(self):
        filter_form_data = self.request.GET.copy()
        filter_form_data.setdefault(
            'start_date',
            timezone.now().date() - timezone.timedelta(days=7))
        filter_form_data.setdefault('end_date', timezone.now().date())
        return ActivityFilterForm(filter_form_data)

    def get(self, request, *args, **kwargs):
        self.filter_form = self.get_filter_form()
        self.filter_form.is_valid()
        return super().get(request, *args, **kwargs)

    def get_search_query(self):
        return self.request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
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
