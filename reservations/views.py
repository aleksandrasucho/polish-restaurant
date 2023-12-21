from django.views import View
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView, DetailView
from .forms import ReservationForm

class HomeView(generic.TemplateView):
    """
    View for the home page.
    """
    template_name = 'home.html'
    
    def get(self, request):
        return render(request, 'home.html', {})
    
class MenuView(generic.TemplateView):
    template_name = 'menu.html'
    
    def get(self, request):
        return render(request, 'menu.html')

class AddReservation(generic.TemplateView):
    template_name = 'add_reservation.html'

    def get(self, request):
        form = ReservationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            # If the form is valid, create a Reservation instance but don't save it to the database yet (commit=False)
            reservation = form.save(commit=False)

            if request.user.is_authenticated:
                reservation.user = request.user

            # Save the reservation to the database
            reservation.save()

            # Redirect to a confirmation page with details of the reservation
            return render(request, 'reservation_confirmation.html', {'reservation': reservation})
        else:
            return render(request, self.template_name, {'form': form})