from django.contrib import admin

from timetracker.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
