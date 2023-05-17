from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdminPanel(admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]
