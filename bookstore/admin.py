from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models


@admin.register(models.Book)
class BookAdminPanel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name", "price", "price_status", "publisher", ]
    search_fields = ["name", "price", "price_status", "publisher", ]

    @admin.display(ordering='price_status')
    def price_status(self, book):
        if book.price < 100:
            return 'Low'
        return "High"
