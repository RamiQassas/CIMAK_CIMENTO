# cimak_app/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('car_number', 'driver_name', 'appointment_date', 'additional_details')