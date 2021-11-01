from django import forms
from .models import Telegrams


class AddTelegram(forms.ModelForm):
    units = [('ALL', 'Виділити всі'), ('A2326', 'A2326'), ('A0355', 'A0355'), ('A1214', 'A1214'),
             ('A0501', 'A0501'), ('A0536', 'A0536'), ('A0693', 'A0693'), ('A1302', 'A1302'), ('A3283', 'A3283'),
             ('A1978', 'A1978'),
             ('A1962', 'A1962'), ('A0563', 'A0563'), ('A1964', 'A1964'), ('A0389', 'A0389'), ('A0591', 'A0591'),
             ('A3336', 'A3336'), ('A1828', 'A1828'),
             ('A3034', 'A3034'), ('A1035', 'A1035'), ('A0943', 'A0943'), ('A1823', 'A1823'), ('A0891', 'A0891'),
             ('A2129', 'A2129'), ('A3139', 'A3139'),
             ('A3750', 'A3750'), ('A1363', 'A1363'), ('A1588', 'A1588'), ('A1361', 'A1361'),
             ('Дн ОТЦК та СП', 'Дн ОТЦК та СП'),
             ('Дон ОТЦК та СП', 'Дон ОТЦК та СП'), ('Зп ОТЦК та СП', 'Зп ОТЦК та СП'),
             ('Хар ОТЦК та СП', 'Хар ОТЦК та СП'), ('Луг ОТЦК та СП', 'Луг  ОТЦК та СП'),
             ('A4226', 'A4226'), ('64 ПУСЗ та ІС', '64 ПУСЗ та ІС'),
             ]
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units, label="Розрахунок розсилки")

    class Meta:
        model = Telegrams
        fields = ('deadline', 'description', 'tlg_scan', 'tlg_number', 'note', 'priority')


class SearchTelegrams(forms.Form):
    search_input = forms.CharField(max_length=100, required=False, label="Номер телеграми")
    confirm = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=[('1', 'Так')], required=False, label="Статус телеграми (виконана/невиконана)")
    priority = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'Низька'), ('1', 'Висока')], required=False, label="Пріорітет телеграми")
    date_create = forms.CharField(max_length=30, required=False, label="Дата створення")







