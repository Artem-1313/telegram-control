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


class SearchTelegrams(forms.Form):
    search_input = forms.CharField(max_length=100, required=False, label="Номер телеграми")
    confirm = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=[('1', 'Так')], required=False, label="Статус телеграми (виконана/невиконана)")
    priority = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'Низька'), ('1', 'Висока')], required=False, label="Пріорітет телеграми")
    date_create = forms.CharField(max_length=30, required=False, label="Дата створення")
    #deadline = forms.CharField(max_length=30, required=False)







