from django.forms import ModelForm
from .models import Day

class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = '__all__'

# class DayEdit(ModelForm):
#     class Meta:
#         model = Day
#         exclude = ['number', 'date', 'activities', 'trip']

