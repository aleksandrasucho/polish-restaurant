from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Provides a list of choices for table capacity.
CAPACITY = ((2, "2"), (4, "4"), (6, "6"), (8, "8"))

# Create your models here.

class Table(models.Model):
    # Table details
    table_number = models.IntegerField(unique=True)
    number_of_seats = models.IntegerField()
    capacity = models.IntegerField(choices=CAPACITY, default=2)
    
    # String representation of a Table instance
    def __str__(self):
        return f"Table {self.table_number} - Seats: {self.number_of_seats}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Basic reservation details
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(null=True, blank=True)
    table = models.ForeignKey(Table, related_name="reservations", on_delete=models.CASCADE, blank=True,)
    number_of_guests = models.IntegerField()
    
    # String representation of a Reservation instance
    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"