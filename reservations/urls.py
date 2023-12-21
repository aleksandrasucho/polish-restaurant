from django.urls import path
from .views import HomeView, MenuView, AddReservation

urlpatterns = [
    path('', HomeView.as_view(), name="base"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('add_reservation/', AddReservation.as_view(), name="reservation" )
]
