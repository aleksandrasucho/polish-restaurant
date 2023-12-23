from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import ReservationForm

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
    form_class = ReservationForm
    success_url = reverse_lazy('reservation')  # Redirect to the 'reservation' URL upon successful form submission

    def form_valid(self, form):
        # If the form is valid, create a Reservation instance but don't save it to the database yet (commit=False)
        reservation = form.save(commit=False)

        if self.request.user.is_authenticated:
            reservation.user = self.request.user

        # Save the reservation to the database
        reservation.save()

        # Pass the reservation object to the success_url template
        self.object = reservation

        return super().form_valid(form)
