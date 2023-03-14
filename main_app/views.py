from django.shortcuts import render, redirect
from .models import Trip, Day, Activity
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import DayForm, ActivityForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta, datetime
from django import forms
import requests

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def trip_index(request):
    trips  = Trip.objects.filter(user=request.user)
    return render(request, 'trips/index.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    days = Day.objects.filter(trip_id=trip_id)
    print(days)
    # res = []
    # for day in days:
    #     if day.city:
    #         response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=2235056e594342b9bfa213839230603&q={day.city}&days=1&aqi=no&alerts=no')
    #         weather = response.json()
    #         res.append(weather)
    #     else:
    #         res.append('')
    # print(res)
    return render(request, 'trips/detail.html', { 'trip': trip})

class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'start']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = '/trips/'

@login_required
def day_detail(request, day_id):
    day = Day.objects.get(id=day_id)
    activity_form = ActivityForm()
    # This makes a request to the weather api for the forecast on the day.
    date_now = datetime.now().date()
    # print(day.date)
    # print(date_now)
    if day.city:
        if day.date < date_now:
            weatherinfo = 'Date is passed'
            weather_icon = ''
        else:
        # if the date is more than 14 days, get future info:
            if day.date > date_now + timedelta(days=14):
                res = requests.get(f'http://api.weatherapi.com/v1/future.json?key=2235056e594342b9bfa213839230603&q={ day.city } {day.country}&dt={day.date}')
                weather = res.json()
                weatherinfo = weather['forecast']['forecastday'][0]['day']
                weather_icon = ''
                # print(weatherinfo)
            # if the date is between now and 14 days, get forecast plus icon:
            elif day.date <= date_now + timedelta(days=14):
                res = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=2235056e594342b9bfa213839230603&q={ day.city } {day.country}&dt={day.date}')
                weather = res.json()
                weatherinfo = weather['forecast']['forecastday'][0]['day']
                weather_icon = weather['forecast']['forecastday'][0]['day']['condition']['icon']
                print(weather_icon)
                # print(weatherf)
            # if the date is today get current weather:
            # elif day.date == date_now:
            #     res = requests.get(f'http://api.weatherapi.com/v1/.json?key=2235056e594342b9bfa213839230603&q={ day.city} { day.country}&aqi=no')
            #     weather = res.json()
            #     # print(weatherf)
            #     weatherf = weather['current']['temp_f']
            #     weather_icon = ['current']['condition']['icon']
            else:
                weatherinfo = 'No data available'
                weather_icon = ''
    else:
        weatherinfo = 'Please add location'
        weather_icon = ''
    # print(res)
    # weather = res.json()
    # print(weather2)
    return render(request, 'days/detail.html', { 'day': day, 'activity_form': activity_form, 'weather': weatherinfo, 'icon': weather_icon} )

@login_required
def days_create(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'days/create.html', {'trip': trip})


# This function will take the input of number of days and create that number of day objects.
# It will auto populate day.number and day.date.
@login_required
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

class DayUpdate(LoginRequiredMixin, UpdateView):
    model = Day
    fields = ['city', 'state', 'country', 'transport', 'lodging', 'flight']

@login_required
def activity_create(request, day_id):
    form = ActivityForm(request.POST)
    new_activity = form.save(commit=False)
    new_activity.save()
    Day.objects.get(id=day_id).activities.add(new_activity.id)
    return redirect('day_detail', day_id=day_id)

@login_required
def activity_detail(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    return render(request, 'activities/detail.html', {'activity': activity})

class ActivityUpdate(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['name', 'time', 'description', 'inout']

# class ActivityDelete(LoginRequiredMixin, DeleteView):
#     model = Activity
#     success_url = reverse_lazy('day_detail')

def activity_delete(request, day_id, activity_id):
    activity = Activity.objects.get(id=activity_id)
    print(activity)
    activity.delete()
    return redirect('day_detail', day_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # this is how to create a user form object that includes data from the browser.
        form = UserCreationForm(request.POST)
        # now we check validity of the form, and handle our success and error situations
        if form.is_valid():
            # we'll add the user to the db
            user = form.save()
            # then we'll log the user in and redirect to our index
            login(request, user)
            return redirect('trip_index')
        else:
            error_message = 'Invalid sign up, try again'
    # a bad POST or GET request will render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
