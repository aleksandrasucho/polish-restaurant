from django.urls import path, include
from .views import HomeView, MenuView, AddReservation, InformationView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('add_reservation/', AddReservation.as_view(), name="add_reservation"),
    path('information/', InformationView.as_view(), name="information"),
    path('accounts/', include('allauth.urls')),
]
