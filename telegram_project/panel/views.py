from django.shortcuts import render
from django.http import HttpResponse
from .models import Telegrams, Executors
from .forms import AddTelegram
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

# Create your views here.


def index(request):
    return render(request, 'panel/index.html' )


class TelegramsListView(ListView):
    model = Telegrams
    template_name = 'panel/index.html'
    context_object_name = "tlg"


    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(TelegramsListView, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['exec'] = Executors.objects.all()
    #     return context


# def show_tlg(request, i):
#     tlg = Telegrams.objects.get(id=i)
#     return render(request, 'panel/show_tlg.html', { 'tlg': tlg.executors_set.all(), 'telega':tlg})


class TelegramDetailView(DetailView):
    model = Telegrams

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TelegramDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        tlg = Telegrams.objects.get(id=self.object.get_id())
        context['tlg'] = tlg.executors_set.all()
        return context




def add_tlg(request):
    if request.method == 'POST':
        form = AddTelegram(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=1)
            description = form.cleaned_data.get('description')
            deadline = form.cleaned_data.get('deadline')
            tlg_scan = form.cleaned_data.get('tlg_scan')
            tlg_number = form.cleaned_data.get('tlg_number')
            note = form.cleaned_data.get('note')

            confirm = form.cleaned_data.get('confirm')
            priority = form.cleaned_data.get('priority')

            tlg = Telegrams(deadline=deadline, description=description, author=user, tlg_scan=tlg_scan, tlg_number=tlg_number, note=note, confirm=confirm, priority=priority)
            tlg.save()

            executors = form.cleaned_data.get('executors')
            for i in executors:
                 tlg.executors_set.create(unit=i)

    else:
        form = AddTelegram()
    return render(request,'panel/add_tlg.html', {'form': form})

