import logging
import datetime
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
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import generic
from django.views.generic import DetailView
from .forms import ReservationForm
from .models import Reservation, Table, UserProfile
from .models import UserProfile


# Set up the logger
logger = logging.getLogger(__name__)


class HomeView(generic.TemplateView):
    """
    Home page view displaying user reservations.
    """

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # Example logic to retrieve user's reservations
        user_reservations = []
        if request.user.is_authenticated:
            user_reservations = Reservation.objects.filter(user=request.user)

        return render(
            request,
            self.template_name,
            {'user_reservations': user_reservations}
        )


class MenuView(generic.TemplateView):
    """
    Menu page view displaying user reservations.
    """

    template_name = 'menu.html'

    def get(self, request):
        user_reservations = []
        if request.user.is_authenticated:
            user_reservations = Reservation.objects.filter(user=request.user)

        return render(
            request,
            'menu.html',
            {'user_reservations': user_reservations}
        )


class ReservationDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View displaying details of a reservation.
    """

    model = Reservation
    template_name = 'reservation_detail.html'
    context_object_name = 'reservation'

    def get(self, request, *args, **kwargs):
        reservation_id = kwargs['pk']

# Ensure that the reservation belongs to the logged-in user and is not cancelled
        reservation = get_object_or_404(
            Reservation, id=reservation_id, user=request.user, cancelled=False
        )

        # Fetch all reservations for the current user
        user_reservations = Reservation.objects.filter(
            user=request.user, cancelled=False
        )

        context = {
            'reservation': reservation,
            'user_reservations': user_reservations,
        }
        return render(request, 'reservation_detail.html', context)

    def post(self, request, *args, **kwargs):
        reservation_id = kwargs['pk']
        
# Ensure that the reservation belongs to the logged-in user and is not cancelled
        reservation = get_object_or_404(
            Reservation, id=reservation_id, user=request.user, cancelled=False
        )


        if 'cancel_reservation' in request.POST:
            if reservation.date >= datetime.date.today():
                reservation.cancelled = True
                reservation.save()
                messages.success(request, "Reservation successfully canceled!")
            else:
                messages.error(request, "Cannot cancel past reservations.")
            
        # Fetch all reservations for the current user after cancellation
        user_reservations = Reservation.objects.filter(
            user=request.user, cancelled=False
        )

        context = {
            'reservation': reservation,
            'user_reservations': user_reservations,
        }

        return render(request, 'reservation_detail.html', context)


class AddReservation(generic.CreateView):
    """
    View for adding a new reservation.
    """

    template_name = 'add_reservation.html'
    form_class = ReservationForm

    def get(self, request, *args, **kwargs):
        # Example logic to retrieve user's reservations
        user_reservations = []
        if request.user.is_authenticated:
            user_reservations = Reservation.objects.filter(user=request.user)

        return render(
            request,
            self.template_name,
            {'form': self.form_class, 'user_reservations': user_reservations}
        )

    def form_valid(self, form):
        reservation = form.save(commit=False)

        if self.request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(
                user=self.request.user
            )

            if created:
                user_profile.role = 2
                user_profile.save()
                
            reservation.user = self.request.user
        else:
            logger.info("User is not authenticated")

        selected_table = self.assign_table(reservation)

        if not selected_table:
            messages.error(
            self.request,
            "No tables available for the selected date and time."
            )

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
        bookings_on_requested_date = Reservation.objects.filter(
            date=date, time=time
        )
        booked_tables = [
            booking.table for booking in bookings_on_requested_date
        ]

        available_tables = [
            table for table in available_tables if table not in booked_tables
        ]


        if not available_tables:
            return None

        return min(available_tables, key=lambda table: table.capacity)


class UpdateReservation(generic.edit.UpdateView):
    """
    View for updating a reservation.
    """

    template_name = 'update_reservation.html'
    model = Reservation
    form_class = ReservationForm
    
    def get_success_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.object.pk})
    
    def get_object(self, queryset=None):
        reservation = super().get_object(queryset=queryset)
        if not (
            self.request.user.is_staff or self.request.user == reservation.user
        ):
            raise PermissionDenied(
                "You are not authorized to edit this reservation."
            )
        return reservation

    def form_valid(self, form):
        date = form.cleaned_data['date']
        time = form.cleaned_data['time']
        guests = form.cleaned_data['number_of_guests']

        messages.success(self.request, f'Booking updated for {guests} guests on {date} at {form.instance.get_time_display()}')
        return super(UpdateReservation, self).form_valid(form)


class DeleteReservation(generic.edit.DeleteView):
    """
    View for deleting a reservation.
    """

    template_name = 'delete_reservation.html'
    model = Reservation
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """This method returns the object that the view will display."""
        reservation = super().get_object(queryset=queryset)
        if self.request.user.is_staff or self.request.user == reservation.user:
            return reservation
        else:
            raise Http404("You are not authorized to edit this reservation.")

    def delete(self, request, *args, **kwargs):
        """
        After the reservation is deleted, this will show a notification
        """
        reservation = self.get_object()
        messages.success(
            self.request,
            f'Booking cancelled for {reservation.number_of_guests} '
            f'guests on {reservation.date} at {reservation.get_time_display()}'
        )
        return super().delete(request, *args, **kwargs)


class InformationView(generic.TemplateView):
    """
    View displaying information.
    """

    template_name = 'information.html'

    def get(self, request, *args, **kwargs):
        # Example logic to retrieve user's reservations
        user_reservations = []
        if request.user.is_authenticated:
            user_reservations = Reservation.objects.filter(user=request.user)

        return render(
        request, 
        self.template_name, 
        {'user_reservations': user_reservations}
        )
