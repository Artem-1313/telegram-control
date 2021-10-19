from django import forms
import datetime
from .models import Telegrams, Executors

class AddTelegram(forms.ModelForm):
    units = [('А1314', 'А1314'), ('A2326', 'A2326'), ('A0355', 'A0355')]
    # date_create = forms.DateTimeField(initial=datetime.date.today, required=False)
    # description = forms.CharField(widget=forms.Textarea)
    # tlg_scan = forms.FileField(upload='tlg_scan_dir/')
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units)
    class Meta:
        model = Telegrams
        fields = ('deadline', 'description', 'tlg_scan', 'tlg_number', 'note', 'confirm', 'priority')

class CheckForms(forms.Form):
    units = [('А1314', 'А1314'), ('A2326', 'A2326'), ('A0355', 'A0355')]
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units)






