from django import forms
import datetime
from .models import Telegrams, Executors

class AddTelegram(forms.ModelForm):
    units = [('A1314', 'A1314'), ('A2326', 'A2326'), ('A0355', 'A0355'), ('A1214', 'A1214'),
              ('A0501', 'A0501')]
    # date_create = forms.DateTimeField(initial=datetime.date.today, required=False)
    # description = forms.CharField(widget=forms.Textarea)
    # tlg_scan = forms.FileField(upload='tlg_scan_dir/')
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units)
    class Meta:
        model = Telegrams
        fields = ('deadline', 'description', 'tlg_scan', 'tlg_number', 'note', 'confirm', 'priority')

class CheckForms(forms.Form):
    units = [('A1314', 'A1314'), ('A2326', 'A2326'), ('A0355', 'A0355'), ('A1214', 'A1214')]
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units)






