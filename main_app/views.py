from django.shortcuts import render, redirect
from .models import Trip, Day, Activity
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import DayForm, ActivityForm
from datetime import timedelta
import requests

# Create your views here.

def home(request):
    return render(request, 'home.html')

def trip_index(request):
    trips  = Trip.objects.filter(user=request.user)
    return render(request, 'trips/index.html', {'trips': trips})

def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    days = Day.objects.filter(trip_id=trip_id)
    print(days)
    res = []
    for day in days:
        if day.city:
            response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=2235056e594342b9bfa213839230603&q={day.city}&days=1&aqi=no&alerts=no')
            weather = response.json()
            res.append(weather)
        else:
            res.append('')
    # print(res)
    return render(request, 'trips/detail.html', { 'trip': trip, 'weather': res})

class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'start']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TripDelete(DeleteView):
    model = Trip
    success_url = '/trips/'

def day_detail(request, day_id):
    day = Day.objects.get(id=day_id)
    activity_form = ActivityForm()
    # This makes a request to the weather api for the forecast on the day.
    res = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=2235056e594342b9bfa213839230603&q={day.city}&days=1&aqi=no&alerts=no')
    weather = res.json()
    # print(weather)
    return render(request, 'days/detail.html', { 'day': day, 'activity_form': activity_form, 'weather': weather} )

def days_create(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'days/create.html', {'trip': trip})


# This function will take the input of number of days and create that number of day objects.
# It will auto populate day.number and day.date.
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

class DayUpdate(UpdateView):
    model = Day
    fields = ['city', 'state', 'country', 'transport', 'lodging', 'flight']

def activity_create(request, day_id):
    form = ActivityForm(request.POST)
    new_activity = form.save(commit=False)
    new_activity.save()
    Day.objects.get(id=day_id).activities.add(new_activity.id)
    return redirect('day_detail', day_id=day_id)

def activity_detail(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    return render(request, 'activities/detail.html', {'activity': activity})

class ActivityUpdate(UpdateView):
    model = Activity
    fields = ['name', 'time', 'description', 'inout']
