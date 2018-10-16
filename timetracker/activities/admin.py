from django.contrib import admin

from timetracker.activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
