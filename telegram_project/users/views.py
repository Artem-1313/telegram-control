from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.



def index(request):
    return HttpResponse("<h1>Hello, world. You're at the main index.</h1>")