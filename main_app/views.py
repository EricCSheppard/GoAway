from django.shortcuts import render, redirect
from .models import Trip, Day, Activity, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import DayForm, ActivityForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta, datetime
from django import forms
import uuid
import boto3
from django.conf import settings
import requests

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL

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
    date_now = datetime.now().date()
    print(days)
    # res = []
    # for day in days:
    #     if day.city:
    #         response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=9da560b0b23b45e4a16160600230604={day.city}&days=1&aqi=no&alerts=no')
    #         weather = response.json()
    #         res.append(weather)
    #     else:
    #         res.append('')
    # print(res)
    return render(request, 'trips/detail.html', { 'trip': trip, 'date_now': date_now})

class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'start']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_form(self):  
        form = super(TripCreate, self).get_form()
        form.fields['start'].widget = forms.DateInput(attrs={'type': 'date'})
        return form 
    
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
        # if date is passed, do not call the api
        if day.date < date_now:
            weatherinfo = ''
            weather_icon = ''
        else:
        # if the date is more than 14 days, get future info:
            if day.date > date_now + timedelta(days=14):
                res = requests.get(f'http://api.weatherapi.com/v1/future.json?key=9da560b0b23b45e4a16160600230604={ day.city } {day.country}&dt={day.date}')
                weather = res.json()
                weatherinfo = weather['forecast']['forecastday'][0]['day']
                weather_icon = ''
                # print(weatherinfo)
            # if the date is between today and 14 days from today, get forecast plus icon:
            elif day.date <= date_now + timedelta(days=14):
                res = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=9da560b0b23b45e4a16160600230604={ day.city } {day.country}&dt={day.date}')
                weather = res.json()
                weatherinfo = weather['forecast']['forecastday'][0]['day']
                weather_icon = weather['forecast']['forecastday'][0]['day']['condition']['icon']
                print(weather_icon)
                # print(weatherf)
            # if the date is today get current weather:
            # elif day.date == date_now:
            #     res = requests.get(f'http://api.weatherapi.com/v1/.json?key=9da560b0b23b45e4a16160600230604={ day.city} { day.country}&aqi=no')
            #     weather = res.json()
            #     # print(weatherf)
            #     weatherf = weather['current']['temp_f']
            #     weather_icon = ['current']['condition']['icon']
            else:
                weatherinfo = ''
                weather_icon = ''
    else:
        weatherinfo = ''
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
        # print('THIS IS THE DAY: ', new_day.as_dict())
        new_day.save()
    return redirect('trip_detail', trip_id=trip_id)

class DayUpdate(LoginRequiredMixin, UpdateView):
    model = Day
    fields = ['city', 'state', 'country', 'transport', 'lodging', 'address', 'flight']

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
    # print(activity)
    activity.delete()
    return redirect('day_detail', day_id)

@login_required
def add_photo(request, trip_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file: 
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, S3_BUCKET, key)
            url = f'{S3_BASE_URL}{S3_BUCKET}/{key}'
            photo = Photo(url=url, trip_id=trip_id)
            photo.save()
        except Exception as error:
            print('Error uploading photo', error)
            return redirect('detail', trip_id=trip_id)

    return redirect('trip_detail', trip_id=trip_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('trip_index')
        else:
            error_message = 'Invalid sign up, try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
