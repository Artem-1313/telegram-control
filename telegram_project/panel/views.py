from django.shortcuts import render
from django.http import HttpResponse
from .models import Telegrams, Executors


# Create your views here.


def index(request):
    return render(request, 'panel/index.html', { 'tlg':Telegrams.objects.all(),'exec':Executors.objects.all()})


