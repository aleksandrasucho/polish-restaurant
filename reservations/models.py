# Import necessary modules and classes
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime

# Provides a list of choices for table capacity.
CAPACITY = ((2, "2"), (4, "4"), (6, "6"), (8, "8"))

# Generate booking times for Monday to Sunday (09:00 - 22:00)
BOOKING_TIME = (
    (datetime.time(12, 0), "12:00pm - 1:45pm"),
    (datetime.time(14, 0), "2:00pm - 3:45pm"),
    (datetime.time(16, 0), "4:00pm - 5:45pm"),
    (datetime.time(18, 0), "6:00pm - 7:45pm"),
    (datetime.time(20, 0), "8:00pm - 9:45pm"),
)

# User profile model, extending the built-in User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(default=2)  # Default role value

# Table model for representing restaurant tables
class Table(models.Model):
    # Table details
    table_number = models.IntegerField(unique=True)  # Ensure table numbers are unique
    number_of_seats = models.IntegerField()
    capacity = models.IntegerField(choices=CAPACITY, default=2)  # Choose from predefined capacity options
    
    # String representation of a Table instance
    def __str__(self):
        return f"Table {self.table_number} - Seats: {self.number_of_seats}"

# Reservation model for storing booking details
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User associated with the reservation
    
    # Basic reservation details
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(choices=BOOKING_TIME, default=datetime.time(12, 0))  # Default booking time
    notes = models.TextField(null=True, blank=True)  # Additional notes (optional)
    table = models.ForeignKey(Table, related_name="reservations", on_delete=models.CASCADE, blank=True,)  # Table associated with the reservation
    number_of_guests = models.IntegerField()  # Number of guests for the reservation
    cancelled = models.BooleanField(default=False)  # Flag indicating whether the reservation is cancelled
    
    # String representation of a Reservation instance
    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"  # Format reservation details for display
