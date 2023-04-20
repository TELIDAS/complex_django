from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models


@admin.register(models.Book)
class BookAdminPanel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name", "price", "publisher"]
    search_fields = ["name", "price", "publisher"]
