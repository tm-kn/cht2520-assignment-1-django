from django.urls import path

from timetracker.activities.views import ActivityListView, NewActivityView

app_name = 'activities'

urlpatterns = [
    path('', ActivityListView.as_view(), name='list'),
    path('new/', NewActivityView.as_view(), name='new'),
]
