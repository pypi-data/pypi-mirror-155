from builtins import str
import csv

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Bank


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank_code', 'branch_code', 'short_name', 'long_name']
    search_fields = ['short_name']
    actions = None

    change_list_template = 'admin/bank/bank_changelist.html'
    import_csv_template = 'admin/bank/bank_import_csv.html'

    def get_urls(self):
        urls = super(BankAdmin, self).get_urls()
        additional_urls = [
            url(r'import-csv/$', self.import_csv),
        ]
        return additional_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            list_reader = list(csv.reader(csv_file))

            try:
                Bank.objects.upsert_from_list_with_header(list_reader)
                self.message_user(request, 'CSV Import Complete')
            except Exception as e:
                self.message_user(request, str(e), level=messages.ERROR)

            return HttpResponseRedirect('/admin/bank/bank')

        form = CsvImportForm()
        payload = {'form': form}
        return render(request, self.import_csv_template, payload)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
