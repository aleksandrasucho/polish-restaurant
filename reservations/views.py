from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Table, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'reservations/index.html'
    context_object_name = 'reservation_list'

    def get_queryset(self):
        return Reservation.objects.filter(date__gte=timezone.now()).order_by('date')
    
class ReservationDetailView(generic.DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'

class ReservationCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Reservation
    template_name = 'reservations/reservation_form.html'
    fields = ['name', 'date', 'time', 'notes', 'table', 'number_of_guests']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReservationUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Reservation
    template_name = 'reservations/reservation_form.html'
    fields = ['name', 'date', 'time', 'notes', 'table', 'number_of_guests']

class ReservationDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Reservation
    success_url = reverse_lazy('reservations:index')
    template_name = 'reservations/reservation_confirm_delete.html'