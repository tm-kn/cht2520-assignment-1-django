from django.urls import path

from timetracker.activities.views import (ActivityCreateView,
                                          ActivityDetailView, ActivityDeleteView,
                                          ActivityListView,
                                          ActivityStopView,
                                          ActivityUpdateView)

app_name = 'activities'

urlpatterns = [
    path('', ActivityListView.as_view(), name='list'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ActivityUpdateView.as_view(), name='update'),
    path('stop/<int:pk>/', ActivityStopView.as_view(), name='stop'),
    path('create/', ActivityCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', ActivityDeleteView.as_view(), name='delete'),
]
