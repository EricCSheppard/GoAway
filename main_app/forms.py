from django.forms import ModelForm
from .models import Day

class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = '__all__'