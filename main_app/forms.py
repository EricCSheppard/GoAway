from django.forms import ModelForm
from .models import Day, Activity, Trip
from django import forms

class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = '__all__'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'time', 'description', 'inout']
        widgets = {
            'time': forms.widgets.DateInput(attrs={'type': 'time'})
        }
        
        
# class TripForm(ModelForm):
#     class Meta:
#         model = Trip
#         fields = ['name', 'start']
#         widgets = {
#             'start': forms.widgets.DateInput(attrs={'type': 'date'})
#         }
