from django import forms
from .models import Appointment, Reminder

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    intervals = forms.MultipleChoiceField(
    choices=Reminder.INTERVAL_CHOICES,  # Assuming the choices are the same
    widget=forms.CheckboxSelectMultiple,
    required=False
    )
    class Meta:
        model = Appointment
        fields = ['name', 'date', 'time', 'email', 'additional_info']
    
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['interval']