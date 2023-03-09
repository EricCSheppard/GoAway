from django.shortcuts import render, redirect
from .models import Trip, Day, Activity
from django.views.generic.edit import CreateView
from .forms import DayForm
from datetime import timedelta

# Create your views here.

def home(request):
    return render(request, 'home.html')

def trip_index(request):
    trips  = Trip.objects.filter(user=request.user)
    return render(request, 'trips/index.html', {'trips': trips})

def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'trips/detail.html', { 'trip': trip})

class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'start']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def day_detail(request, day_id):
    day = Day.objects.get(id=day_id)
    return render(request, 'days/detail.html', { 'day': day})

def days_create(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'days/create.html', {'trip': trip})

def days_populate(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    # print('This is the trip: ', trip)
    day_num = int(request.POST['day_num'])
    # print('THIS IS THE NUMBER:', day_num)
    for i in range(day_num):
        day = DayForm()
        new_day = day.save(commit=False)
        new_day.number = (i + 1)
        new_day.date = trip.start
        if i > 0:
            new_day.date += timedelta(days=i)
        new_day.trip_id = trip_id
        print('THIS IS THE DAY: ', new_day.as_dict())
        new_day.save()
    return redirect('trip_detail', trip_id=trip_id)
