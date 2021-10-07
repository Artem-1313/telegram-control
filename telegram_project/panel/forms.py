from django import forms
import datetime


class AddTelegram(forms.Form):
    units= [('А1314', 'А1314'), ('A2326', 'A2326'), ('A0355', 'A0355')]
    date_create = forms.DateTimeField(initial=datetime.date.today)
    description = forms.CharField(widget=forms.Textarea)
    executors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=units)


    # class Meta:
    #     fields = ['date_create','description']

