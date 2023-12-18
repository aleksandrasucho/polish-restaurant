from django.urls import path
from .views import HomeView, MenuView

urlpatterns = [
    path('', HomeView.as_view(), name="base"),
    path('menu/', MenuView.as_view(), name="menu"),
]
