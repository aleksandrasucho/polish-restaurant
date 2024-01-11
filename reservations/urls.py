from django.urls import path, include
from .views import (
    HomeView,
    MenuView,
    AddReservation,
    InformationView,
    UpdateReservation,
    DeleteReservation,
    ReservationDetailView,
)

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('add_reservation/', AddReservation.as_view(), name="add_reservation"),
    path('information/', InformationView.as_view(), name="information"),
    path('accounts/', include('allauth.urls')),
    path(
    'update_reservation/<int:pk>/', 
    UpdateReservation.as_view(),
    name="update_reservation"
),
    path(
    'delete_reservation/<int:pk>/', 
    DeleteReservation.as_view(), 
    name="delete_reservation"
),
    path(
    'reservation/<int:pk>/', 
    ReservationDetailView.as_view(), 
    name='reservation_detail'
),
]