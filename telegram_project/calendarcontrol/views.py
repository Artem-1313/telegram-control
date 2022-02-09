from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy

from .forms import ModalForm
from .models import telegramsControl
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


# Create your views here.


@login_required
#@require_http_methods(["POST"])
def index(request):
	events = telegramsControl.objects.filter(author_id=request.user.id)
	if request.method == 'POST':
		form=ModalForm(request.POST, request.FILES)
		print(111)
		if form.is_valid():

			form.instance.author_id=request.user.id
			form.save()
			return redirect('calendarcontrol:index')
	else:
		form = ModalForm(request.POST)

	return render(request,"calendarcontrol/calendar.html", {'form':form, 'title':events})


class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = telegramsControl

	def test_func(self):
		if self.get_object().author == self.request.user:
			return True
		return False

@login_required
def test(request, pk):
		if request.method=="POST":
			db = telegramsControl.objects.get(id=pk)

			if (request.POST.getlist('test1')):
				db.confirm = True
				db.save()
			else:
				db.confirm = False
				db.save()

		return HttpResponse("calendarcontrol:index")

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = telegramsControl
	template_name = "calendarcontrol/telegramscontrol_update.html"
	fields = ('date', 'unit_to_report','tlg_number','description','priority','tlg_scan')

	def test_func(self):
		if self.get_object().author == self.request.user:
			return True
		return False

	def get_success_url(self):
		return reverse_lazy('calendarcontrol:index')

class EventDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
	model = telegramsControl
	success_url = "/control_up/"

	def test_func(self):
		if self.get_object().author == self.request.user:
			return True
		return False


@login_required
def pdf_view(request, pk):
    try:
        tlg = telegramsControl.objects.get(id=pk)
        return HttpResponse(open(str(tlg.tlg_scan), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

