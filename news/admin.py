from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models


@admin.register(models.News)
class NewsAdminPanel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["link"]
    search_fields = ["link"]
