from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models


class UserAdminPanel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("username", "email")


admin.site.register(models.User, UserAdminPanel)
