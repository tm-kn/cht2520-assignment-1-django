from django.urls import path

from timetracker.activities.views import (ActivityCreateView,
                                          ActivityDetailView, ActivityListView,
                                          ActivityStopView)

app_name = 'activities'

urlpatterns = [
    path('', ActivityListView.as_view(), name='list'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='detail'),
    path('stop/', ActivityStopView.as_view(), name='stop'),
    path('create/', ActivityCreateView.as_view(), name='create'),
]
