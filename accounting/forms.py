from django import forms
from .models import HistoryRecord


class HistoryRecordForm(forms.ModelForm):
    class Meta:
        model = HistoryRecord
        fields = '__all__'
