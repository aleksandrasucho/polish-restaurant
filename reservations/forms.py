from django import forms
from django.forms import DateInput
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation, Table

class ReservationForm(forms.ModelForm):
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Reservation
        fields = [
            'name', 'customer_email', 'date', 'time',
            'notes', 'number_of_guests'
        ]
        
        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
                'date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            }
        
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')

        # Check if the selected date is in the future
        if date < timezone.now().date():
            raise ValidationError('Sorry, you have to book a future date')

        # Check if there are tables available for the selected date and time
        if not Table.objects.filter(reservations__date=date, reservations__time=time).exists():
            raise ValidationError('Sorry, no tables available for the selected date and time')

        # Check if there are tables with sufficient capacity for the number of guests
        available_tables = Table.objects.filter(capacity__gte=number_of_guests)
        if not available_tables.exists():
            raise ValidationError('Sorry, no tables with sufficient capacity available')
