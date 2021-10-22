from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Telegrams, Executors
from .forms import AddTelegram, CheckForms
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
import os

# Create your views here.


# def index(request):
#     return render(request, 'panel/index.html')


class TelegramsListView(LoginRequiredMixin, ListView) :
    model = Telegrams
    template_name = 'panel/index.html'
    #context_object_name = "tlg"
    #queryset = Telegrams.objects.filter(author_id=2)
    ordering = ['-date_create']

    def get_context_data(self,  **kwargs):
        context = super(TelegramsListView, self).get_context_data(**kwargs)
        context['tlg'] = Telegrams.objects.filter(author_id=self.request.user.id)
        return context



class TelegramDetailView(LoginRequiredMixin, DetailView):
    model = Telegrams

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TelegramDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        tlg = Telegrams.objects.get(id=self.object.get_id())
        context['tlg'] = tlg.executors_set.all()
        return context


class TelegramsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Telegrams
    success_url = "/panel/"

    def test_func(self):
        tlg = self.get_object()
        print(tlg)
        if self.request.user == tlg.author:
            return True
        return False


class TelegramsUpdateView(LoginRequiredMixin,  UserPassesTestMixin, UpdateView):
    model = Telegrams
    # form_class = AddTelegram
    success_url = "/panel/"
    template_name = "panel/telegrams_update.html"
    fields = ['description', 'deadline', 'tlg_scan', 'tlg_number', 'note', 'confirm', 'priority', ]


    @property
    def get_units_db(self):
        tlg = Telegrams.objects.get(id=self.object.get_id())
        self.tlg_output = Telegrams.objects.get(id=self.object.get_id())
        tlg_executors = tlg.executors_set.all()
        tlg_exec_list = []
        for i in tlg_executors:
            tlg_exec_list.append(i.unit)
        # print(i.unit)
        return tlg_exec_list

    def test_func(self):
        tlg = self.get_object()
        if self.request.user == tlg.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TelegramsUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        tlg_exec_list = self.get_units_db
        context['list'] = ['A2326', 'A0355', 'A1314', 'A1214', 'A0501']
        context['ttt'] = tlg_exec_list
        return context

    def form_valid(self, form):
        units_test = self.request.POST.getlist('test1')
        units_db = self.get_units_db
        select_units = self.request.POST.getlist('test')

        # required for checkboxes
        if len(units_test) == 0 and len(select_units) == 0:
            messages.warning(self.request, 'error')
            return redirect('telegram-update', self.object.get_id())
        # delete executors-units from db
        if list(set(units_db).symmetric_difference(set(units_test))):
            print("DELETE")
            print(set(units_db).symmetric_difference(set(units_test)))
            l = list(set(units_db).symmetric_difference(set(units_test)))
            for i in l:
                Executors.objects.filter(telegrams_id=self.object.get_id(), unit=i).delete()

        # add executors-units to db
        if select_units:
            print("ADD")
            print(select_units)
            for i in select_units:
                self.tlg_output.executors_set.create(unit=i)
        # section update telegram information
        description = form.cleaned_data.get('description')
        deadline = form.cleaned_data.get('deadline')
        tlg_scan = form.cleaned_data.get('tlg_scan')
        tlg_number = form.cleaned_data.get('tlg_number')
        note = form.cleaned_data.get('note')
        confirm = form.cleaned_data.get('confirm')
        priority = form.cleaned_data.get('priority')
        if tlg_scan != self.tlg_output.tlg_scan:
            print(tlg_scan)
            print(True)
            if os.path.exists(str(self.tlg_output.tlg_scan)):
                os.remove(str(self.tlg_output.tlg_scan))
            form.save()
        form.save()

        return redirect('panel-home')

@login_required()
def CheckUnits(request, pk):
    tlg = Telegrams.objects.get(id=pk)
    ttt = tlg.executors_set.all()
    print(tlg.id)
    if request.method == 'POST':
        for i in ttt:
            print(f"{i.unit}+{i.status}")
            Executors.objects.filter(telegrams_id=tlg.id, unit=i.unit).update(status=False)
        sss = request.POST
        print(sss.getlist('test'))

        for i in sss.getlist('test'):
            print(i)
            Executors.objects.filter(telegrams_id=tlg.id, unit=i).update(status=True)

    return render(request, 'panel/telegrams_check.html', {'ttt': ttt, })


@login_required
def add_tlg(request):
    if request.method == 'POST':
        form = AddTelegram(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)

            description = form.cleaned_data.get('description')
            deadline = form.cleaned_data.get('deadline')
            tlg_scan = form.cleaned_data.get('tlg_scan')
            tlg_number = form.cleaned_data.get('tlg_number')
            note = form.cleaned_data.get('note')
            confirm = form.cleaned_data.get('confirm')
            priority = form.cleaned_data.get('priority')

            tlg = Telegrams(deadline=deadline, description=description, author=user, tlg_scan=tlg_scan,
                            tlg_number=tlg_number, note=note, confirm=confirm, priority=priority)
            tlg.save()

            executors = form.cleaned_data.get('executors')
            for i in executors:
                tlg.executors_set.create(unit=i)

    else:
        form = AddTelegram()
    return render(request, 'panel/add_tlg.html', {'form': form})
