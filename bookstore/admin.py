import csv
import io

from django.contrib import admin
from django.db.models import Avg
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from . import models
from .decorator import query_debugger


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(models.Book)
class BookAdminPanel(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["name", "price", "price_status", "publisher", "avr_price_of_publisher"]
    search_fields = ["name", "price"]
    actions = ["export_as_csv"]
    change_list_template = "entities/tab_changelist.html"

    @admin.display(ordering='price_status')
    def price_status(self, book):
        if book.price < 100:
            return 'Low'
        return "High"

    @query_debugger
    @admin.display(ordering="Average-Price of Publisher")
    def avr_price_of_publisher(self, book):
        queryset = models.Book.objects.filter(publisher__id=book.publisher_id).annotate(avg_price=Avg("price"))
        for data in queryset:
            return data.avg_price

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        data = dict()
        data_for_save = list()
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            lines = csv.reader(io_string, delimiter=';', quotechar='|')
            for line in lines:
                splitted = (line[0].split(","))
                if splitted[0] == "id":
                    pass
                else:
                    data = {
                        "name": splitted[1],
                        "price": splitted[2],
                        "publisher": splitted[3],
                    }

                    data_for_save.append(data)
            try:
                models.Book.objects.bulk_create([models.Book(**{
                    'name': url.get("name"),
                    'price': url.get("price"),
                    'publisher': models.Publisher.objects.get(name=url.get("publisher")),
                }) for url in data_for_save])
            except models.Publisher.DoesNotExist:
                models.Book.objects.bulk_create([models.Book(**{
                    'name': url.get("name"),
                    'price': url.get("price"),
                    'publisher': None,
                }) for url in data_for_save])

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    def has_add_permission(self, request):
        return False
