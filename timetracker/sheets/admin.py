from django.contrib import admin

from timetracker.sheets.models import Sheet


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    pass
