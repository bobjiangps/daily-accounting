from django import forms
from .models import HistoryRecord, TransferRecord


class HistoryRecordForm(forms.ModelForm):
    class Meta:
        model = HistoryRecord
        # fields = '__all__'
        exclude = ['created_date', 'updated_date']


class TransferRecordForm(forms.ModelForm):
    class Meta:
        model = TransferRecord
        exclude = ['created_date', 'updated_date', 'currency']
