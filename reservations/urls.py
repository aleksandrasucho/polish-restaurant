from django.urls import path, include
from .views import HomeView, MenuView, AddReservation

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('add_reservation/', AddReservation.as_view(), name="add_reservation"),
    path('accounts/', include('allauth.urls')),
]
