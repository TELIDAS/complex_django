from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models


class NewsAdminPanel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("link",)


admin.site.register(models.News, NewsAdminPanel)
