from django.urls import path
from .views import HomeView, MenuView, AddReservation, LogoutRedirectView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('add_reservation/', AddReservation.as_view(), name="reservation" ),
    path('logout/', LogoutRedirectView.as_view(), name="logout"),
]
