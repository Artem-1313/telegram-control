from django import forms
from .models import Telegrams, Executors


class AddTelegram(forms.ModelForm):
    units = [('A1314', 'A1314'), ('A2326', 'A2326'), ('A0355', 'A0355'), ('A1214', 'A1214'),
              ('A0501', 'A0501')]
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units, label="Розрахунок розсилки")

    class Meta:
        model = Telegrams
        fields = ('deadline', 'description', 'tlg_scan', 'tlg_number', 'note', 'priority')


class CheckForms(forms.Form):
    units = [('A1314', 'A1314'), ('A2326', 'A2326'), ('A0355', 'A0355'), ('A1214', 'A1214')]
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units)







