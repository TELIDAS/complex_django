from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models


@admin.register(models.User)
class UserAdminPanel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]
