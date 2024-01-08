from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from .forms import ReservationForm
from .models import Reservation, Table, CAPACITY, BOOKING_TIME

class HomeView(generic.TemplateView):
    template_name = 'home.html'
    
    def get(self, request):
        return render(request, 'home.html', {})

class MenuView(generic.TemplateView):
    template_name = 'menu.html'
    
    def get(self, request):
        return render(request, 'menu.html')

@method_decorator(login_required(login_url='account_login'), name='dispatch')
class AddReservation(generic.CreateView):
    """View to handle the addition of reservations."""
    template_name = 'add_reservation.html'
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = self.form_class()
                return render(
                    request,
                    self.template_name,
                    {'form': form},
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def form_valid(self, form):
        """Handle form validation for adding a reservation."""
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateReservation(generic.edit.UpdateView):
    template_name = 'update_reservation.html'
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:view')

    def get_object(self, queryset=None):
        reservation = super().get_object(queryset=queryset)
        if self.request.user.is_staff or self.request.user == reservation.user:
            return reservation
        else:
            raise Http404("You are not authorized to edit this reservation.")

    def form_valid(self, form):
        date = form.cleaned_data['date']
        time = form.cleaned_data['time']
        guests = form.cleaned_data['number_of_guests']

        messages.success(self.request, f'Booking updated for {guests} guests on {date} at {form.instance.get_time_display()}')
        return super(UpdateReservation, self).form_valid(form)

class DeleteReservation(generic.edit.DeleteView):
    template_name = 'delete_reservation.html'
    model = Reservation
    success_url = reverse_lazy('reservation:view')

    def get_object(self, queryset=None):
        reservation = super().get_object(queryset=queryset)
        if self.request.user.is_staff or self.request.user == reservation.user:
            return reservation
        else:
            raise Http404("You are not authorized to edit this reservation.")

    def delete(self, request, *args, **kwargs):
        reservation = self.get_object()
        messages.success(self.request, f'Booking cancelled for {reservation.number_of_guests} guests on {reservation.date} at {reservation.get_time_display()}')
        return super().delete(request, *args, **kwargs)

class InformationView(generic.TemplateView):
    template_name = 'information.html'