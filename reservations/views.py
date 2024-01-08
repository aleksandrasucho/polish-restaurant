import logging
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView
from .forms import ReservationForm
from .models import Reservation, Table

# Set up the logger
logger = logging.getLogger(__name__)

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, 'home.html', {})

class MenuView(generic.TemplateView):
    template_name = 'menu.html'

    def get(self, request):
        return render(request, 'menu.html')

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation_detail.html'
    context_object_name = 'reservation'

@method_decorator(login_required(login_url='account_login'), name='dispatch')
class AddReservation(generic.CreateView):
    template_name = 'add_reservation.html'
    form_class = ReservationForm

    def form_valid(self, form):
        reservation = form.save(commit=False)

        if self.request.user.is_authenticated:
            logger.info("User is authenticated: %s", self.request.user)
            reservation.user = self.request.user
        else:
            logger.info("User is not authenticated")

        selected_table = form.cleaned_data.get('table', None)
        if selected_table:
            reservation.table = selected_table
        else:
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            guests = form.cleaned_data['number_of_guests']

            tables_with_capacity = list(Table.objects.filter(
                capacity__gte=guests
            ))

            bookings_on_requested_date = Reservation.objects.filter(
                date=date, time=time)

            for booking in bookings_on_requested_date:
                for table in tables_with_capacity:
                    if table.table_number == booking.table.table_number:
                        tables_with_capacity.remove(table)
                        break
            
            if not tables_with_capacity:
                messages.error(self.request, "No tables available for the selected date and time.")
                return render(self.request, self.template_name, {'form': form})

            lowest_capacity_table = min(tables_with_capacity, key=lambda table: table.capacity)
            reservation.table = lowest_capacity_table

        reservation.save()

        self.success_url = reverse_lazy('reservation_detail', kwargs={'pk': reservation.pk})
        self.object = reservation

        return super().form_valid(form)

class UpdateReservation(generic.edit.UpdateView):
    template_name = 'update_reservation.html'
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:view')

    def get_object(self, queryset=None):
        reservation = super().get_object(queryset=queryset)
        if not (self.request.user.is_staff or self.request.user == reservation.user):
            raise PermissionDenied("You are not authorized to edit this reservation.")
        return reservation

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
        if not (self.request.user.is_staff or self.request.user == reservation.user):
            raise PermissionDenied("You are not authorized to edit this reservation.")
        return reservation

    def delete(self, request, *args, **kwargs):
        reservation = self.get_object()
        messages.success(self.request, f'Booking cancelled for {reservation.number_of_guests} guests on {reservation.date} at {reservation.get_time_display()}')
        return super().delete(request, *args, **kwargs)

class InformationView(generic.TemplateView):
    template_name = 'information.html'