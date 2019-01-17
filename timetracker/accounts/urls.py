from django.urls import include, path

from timetracker.accounts.views import RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]
