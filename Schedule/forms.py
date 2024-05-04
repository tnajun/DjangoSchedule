
from django import forms
from .models import ScheduleAvailability


class ScheduleAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ScheduleAvailability
        fields = ['day_of_week', 'start_time', 'end_time']

