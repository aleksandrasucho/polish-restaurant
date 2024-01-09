import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views import generic
from django.views.generic import DetailView
from .forms import ReservationForm
from .models import Reservation, Table, UserProfile
from .models import UserProfile

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

class ReservationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Reservation
    template_name = 'reservation_detail.html'
    context_object_name = 'reservation'

    def get(self, request, *args, **kwargs):
        reservation_id = kwargs['pk']
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        context = {
            'reservation': reservation,
        }
        return render(request, 'reservation_detail.html', context)

class AddReservation(generic.CreateView):
    template_name = 'add_reservation.html'
    form_class = ReservationForm

    def form_valid(self, form):
        reservation = form.save(commit=False)

        if self.request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)

            if created:
                user_profile.role = 2
                user_profile.save()

            logger.info("User is authenticated: %s", self.request.user)
            reservation.user = self.request.user
        else:
            logger.info("User is not authenticated")

        selected_table = self.assign_table(reservation)

        if not selected_table:
            messages.error(self.request, "No tables available for the selected date and time.")
            return render(self.request, self.template_name, {'form': form})

        reservation.table = selected_table
        reservation.save()

        messages.success(self.request, "Reservation successfully created!")

        # Redirect to a different URL (PRG pattern)
        return redirect('reservation_detail', pk=reservation.pk)

    def assign_table(self, reservation):
        date = reservation.date
        time = reservation.time
        guests = reservation.number_of_guests

        available_tables = Table.objects.filter(capacity__gte=guests)
        bookings_on_requested_date = Reservation.objects.filter(date=date, time=time)
        booked_tables = [booking.table for booking in bookings_on_requested_date]
        available_tables = [table for table in available_tables if table not in booked_tables]

        if not available_tables:
            return None

        return min(available_tables, key=lambda table: table.capacity)

class UpdateReservation(generic.edit.UpdateView):
    template_name = 'update_reservation.html'
    model = Reservation
    form_class = ReservationForm
    
    def get_success_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.object.pk})
    
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
    success_url = reverse_lazy('reservation:detail')

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