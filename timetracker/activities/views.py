from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from timetracker.activities.forms import ActivityForm
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

    def get_success_url(self):
        return reverse_lazy('activities:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ActivityListView(LoginRequiredMixin, ActivityQuerySetMixin, ListView):
    def get_queryset(self):
        return super().get_queryset().filter(
            start_datetime__gte=self.get_start_of_range(),
            start_datetime__lte=self.get_end_of_range())

    def get_start_of_range(self):
        # Default to 7 days ago.
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        return seven_days_ago.replace(hour=0, minute=0, second=0)

    def get_end_of_range(self):
        # Default to tonight 23:59:59.
        return timezone.now().replace(hour=23, minute=59, second=59)


class ActivityDetailView(LoginRequiredMixin, ActivitySingleObjectMixin,
                         DetailView):
    pass


class ActivityStopView(ActivitySingleObjectMixin, View):
    def post(self, *args, **kwargs):
        obj = self.get_object()
        obj.stop()
        return redirect('activities:list')


class ActivityDeleteView(ActivitySingleObjectMixin, DeleteView):
    success_url = reverse_lazy('activities:list')
