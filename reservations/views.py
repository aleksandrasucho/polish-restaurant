from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.shortcuts import render
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
    template_name = 'add_reservation.html'
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('home')  # Use the correct name for the 'home' view

    def form_valid(self, form):
        reservation = form.save(commit=False)

        # Retrieve date and time from cleaned_data
        date = form.cleaned_data.get('date')
        time = form.cleaned_data.get('time')

        # Check if the selected table is available for the specified date and time
        if reservation.table and Reservation.objects.filter(table=reservation.table, date=date, time=time).exists():
            # Table is already booked at the specified date and time
            raise ValidationError('Sorry, the selected table is not available for the specified date and time.')

        # Get the selected table from the form and assign it to the reservation
        selected_table = form.cleaned_data.get('table', None)
        if selected_table:
            reservation.table = selected_table
        else:
            # Assign table with the lowest capacity
            guests = form.cleaned_data['number_of_guests']

            # Filter tables with capacity greater or equal to the number of guests
            tables_with_capacity = list(Table.objects.filter(
                capacity__gte=guests
            ))

            # Get bookings on specified date and time
            bookings_on_requested_date = Reservation.objects.filter(
                date=date, time=time)

            # Iterate over bookings to get tables not booked
            for booking in bookings_on_requested_date:
                for table in tables_with_capacity:
                    if table.table_number == booking.table.table_number:
                        tables_with_capacity.remove(table)
                        break
            
            if tables_with_capacity:
                lowest_capacity_table = min(tables_with_capacity, key=lambda table: table.capacity)
                reservation.table = lowest_capacity_table
            else:
                pass

        # Save the reservation to the database
        reservation.save()

        # Pass the reservation object to the success_url template
        self.object = reservation

        return super().form_valid(form)

class InformationView(generic.TemplateView):
    template_name = 'information.html'