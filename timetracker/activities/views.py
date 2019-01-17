from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from timetracker.activities.forms import ActivityForm
from timetracker.activities.models import Activity


class ActivityCreateView(LoginRequiredMixin, CreateView):
    form_class = ActivityForm
    template_name = 'activities/activity_create.html'

    def get_success_url(self):
        return reverse_lazy('activities:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
