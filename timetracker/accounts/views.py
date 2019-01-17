from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from timetracker.accounts.forms import RegistrationForm


class RegistrationView(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        # User already logged in
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log registered user in
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'])
        assert user is not None
        login(self.request, user)
        return response
