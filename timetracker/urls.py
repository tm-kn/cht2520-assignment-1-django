from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from timetracker.home.views import HomepageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('activities/',
         include('timetracker.activities.urls', namespace='activities')),
    path('', HomepageView.as_view(), name='home')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
