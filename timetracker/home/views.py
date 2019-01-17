from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView


class HomepageView(LoginRequiredMixin, RedirectView):
    pattern_name = 'activities:list'
