from django.forms import ModelForm
from .models import Day,Activity

class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = '__all__'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'time', 'description', 'inout']

