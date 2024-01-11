from django import forms
from django.forms import DateInput, Select
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from .models import Reservation, Table, CAPACITY, BOOKING_TIME


class ReservationForm(forms.ModelForm):
    # Customizing the time field with a dropdown
    time = forms.ChoiceField(
        choices=BOOKING_TIME,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = [
            'name', 'date', 'time', 'notes', 'number_of_guests', 'table'
        ]

        # Customizing the appearance of form fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'number_of_guests': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                    'min': 1,
                    'max': 8
                }
            ),
            'table': forms.Select(attrs={'class': 'form-control'}),
        }

        # Custom labels for form fields
        labels = {
            'name': 'Full Name',
        }

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')
        selected_table = cleaned_data.get('table')

        # Check if the selected date is in the future
        if date < timezone.now().date():
            self.add_error('date', 'Sorry, you have to book a future date')

        # Check if there are reservations for the selected date and time
        if Reservation.objects.filter(date=date, time=time).exists():
            self.add_error(
                'date',
                'Sorry, no tables available for the selected date and time'
            )

# Check if there are tables with sufficient capacity for the number of guests
        available_tables = Table.objects.filter(capacity__gte=number_of_guests)
        if not available_tables.exists():
            self.add_error(
                'number_of_guests',
                'Sorry, no tables with sufficient capacity available'
            )

        return cleaned_data  # Return the cleaned data after validation