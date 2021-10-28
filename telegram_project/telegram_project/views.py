from django.shortcuts import render, redirect


def index(request):
    return redirect('login')


def error_404_view(request, exception=None):
    return render(request, 'telegram_project/404.html', status=400)

def error_403_view(request, exception=None):
    return render(request, 'telegram_project/403.html', status=400)
