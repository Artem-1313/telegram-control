from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse, Http404, HttpResponse, response
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Telegrams, Executors
from .forms import AddTelegram, SearchTelegrams
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
import os


# Create your views here.


# def index(request):
#     return render(request, 'panel/index.html')


class TelegramsListView(LoginRequiredMixin, ListView):
    model = Telegrams
    template_name = 'panel/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Telegrams.objects.all().filter(author_id=self.request.user.id, confirm=False).order_by('-deadline')


class TelegramsArchive(LoginRequiredMixin, ListView):
    model = Telegrams
    template_name = 'panel/archive.html'
    paginate_by = 10

    def get_queryset(self):
        return Telegrams.objects.all().filter(author_id=self.request.user.id).order_by('-deadline')


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


class TelegramsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Telegrams
    # form_class = AddTelegram
    success_url = "/panel/"
    template_name = "panel/telegrams_update.html"
    fields = ['description', 'deadline', 'tlg_scan', 'tlg_number', 'note', 'confirm', 'priority', ]

    @property
    def get_units_db(self):
        tlg = Telegrams.objects.get(id=self.object.get_id())
        #tlg = get_object_or_404(Telegrams, id=self.object.get_id())
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

        context['list'] = ['A2326', 'A0355', 'A1214', 'A0501', 'A0536', 'A0693', 'A1302', 'A3283',
                           'A1978', 'A1962', 'A0563', 'A1964', 'A0389', 'A0591', 'A3336', 'A1828', 'A3034', 'A1035', 'A0943',
                           'A1823', 'A0891', 'A2129', 'A3139', 'A3750', 'A1363', 'A1588', 'A1361',
                           'Дн ОТЦК та СП', 'Дон ОТЦК та СП', 'Зп ОТЦК та СП', 'Хар ОТЦК та СП', 'Луг ОТЦК та СП', 'A4226', '64 ПУСЗ та ІС']
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
            for i in select_units:
                self.tlg_output.executors_set.create(unit=i)
        # section update telegram information

        tlg_scan = form.cleaned_data.get('tlg_scan')

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
    if request.method == 'POST':
        for i in ttt:
            Executors.objects.filter(telegrams_id=tlg.id, unit=i.unit).update(status=False)
        sss = request.POST

        for i in sss.getlist('test'):
            Executors.objects.filter(telegrams_id=tlg.id, unit=i).update(status=True)
        print(f"Усього тлг --> {len(Executors.objects.filter(telegrams_id=tlg.id).all())}, де виконано --> {len(Executors.objects.filter(telegrams_id=tlg.id, status=True).all())}")
        if len(Executors.objects.filter(telegrams_id=tlg.id).all()) == len(Executors.objects.filter(telegrams_id=tlg.id, status=True).all()):
            print("Всі виконали")
            tlg.confirm = True
            tlg.save()
        else:
            tlg.confirm = False
            tlg.save()
            print("Не всі виконані")
        return redirect('panel-home')

    return render(request, 'panel/telegrams_check.html', {'ttt': ttt, "tlg": tlg})


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
            # confirm = form.cleaned_data.get('confirm')
            priority = form.cleaned_data.get('priority')

            tlg = Telegrams(deadline=deadline, description=description, author=user, tlg_scan=tlg_scan,
                            tlg_number=tlg_number, note=note, priority=priority)
            tlg.save()

            executors = form.cleaned_data.get('executors')
            for i in executors:
                if i != 'ALL':
                    tlg.executors_set.create(unit=i)

            return redirect('panel-home')

    else:
        form = AddTelegram()
    return render(request, 'panel/add_tlg.html', {'form': form})


@login_required()
def pdf_view(request, pk):
    try:

        tlg = Telegrams.objects.get(id=pk)
        return HttpResponse(open(str(tlg.tlg_scan), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


@login_required()
def search_by_unit(request, name):
    ex = Executors.objects.filter(unit=name)
    ex_status_true = Executors.objects.filter(unit=name, status=True).count()
    ex_status_false = Executors.objects.filter(unit=name, status=False).count()

    sum_ = ex_status_true + ex_status_false
    return render(request, 'panel/units_detail_tlg.html', {"units": ex, "name": name,
                                                           "ex_status_true": ex_status_true,
                                                           "ex_status_false": ex_status_false,
                                                           "sum_": sum_})


class TelegramsSearchView(FormView):
    template_name = 'panel/search.html'
    model = Telegrams
    form_class = SearchTelegrams
    success_url = "/panel/"

    def get_context_data(self, **kwargs):
        context = super(TelegramsSearchView, self).get_context_data(**kwargs)
        context['search_text'] = self.get_queryset()
        return context

    def get_queryset(self, **kwargs):
        name = self.request.GET.get('search_input', '')
        date_create = self.request.GET.get('date_create', '2021-10-26 - 2021-10-29')
        confirm: object = self.request.GET.get('confirm')
        priority = self.request.GET.get('priority')
        print(confirm)
        
        if not confirm: confirm = 0
       
        def check_dates(input_):

            l = input_.split(" ")

            if l[0] == l[2]:
                d1 = l[0] + " 00:00:01"
                d2 = l[0] + " 23:59:59"
                return [d1, d2]
            else:
                return [l[0], l[2]]

        x = check_dates(date_create)

        return Telegrams.objects.filter(Q(tlg_number__icontains=name) & Q(date_create__range=x) & Q(confirm=confirm) & Q(priority=priority))

