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
    success_url = reverse_lazy('home.html')

    def form_valid(self, form):
        reservation = form.save(commit=False)

        if self.request.user.is_authenticated:
            print("User is authenticated:", self.request.user)
            reservation.user = self.request.user
        else:
            print("User is not authenticated")

        # Save the reservation to the database
        reservation.save()

        # Pass the reservation object to the success_url template
        self.object = reservation

        return super().form_valid(form)