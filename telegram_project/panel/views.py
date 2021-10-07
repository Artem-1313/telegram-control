from django.shortcuts import render
from django.http import HttpResponse
from .models import Telegrams, Executors
from .forms import AddTelegram


# Create your views here.


def index(request):
    return render(request, 'panel/index.html', { 'tlg':Telegrams.objects.all(),'exec':Executors.objects.all()})


def show_tlg(request, i):
    tlg = Telegrams.objects.get(id=i)
    return render(request, 'panel/show_tlg.html', { 'tlg': tlg.executors_set.all(), 'description':tlg.description})


def add_tlg(request):
    form = AddTelegram()
    return render(request,'panel/add_tlg.html', {'form': form})

