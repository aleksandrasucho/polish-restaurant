from django.urls import path
from .views import HomeView, MenuView, ReservationView

urlpatterns = [
    path('', HomeView.as_view(), name="base"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('create_reservation/', ReservationView.as_view(), name="reservation" )
]
