from django.contrib import admin
from . import models


@admin.register(models.News)
class NewsAdminPanel(admin.ModelAdmin):
    list_display = ["link"]
    search_fields = ["link"]
