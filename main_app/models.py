from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

TRANSPORT = (
    ('W', 'Walk'),
    ('B', 'Bike'),
    ('D', 'Drive'),
    ('T', 'Train'),
    ('F', 'Fly')
)

TIMES = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)

class Activity(models.Model):
    name = models.CharField(max_length=50)
    time = models.CharField(
        max_length=1,
        choices = TIMES,
        default = TIMES[0][1]
    )
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name


class Trip(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Trip to {self.name} on {self.start}'
    
    def get_absolute_url(self):
        return reverse('days_create', kwargs={'trip_id': self.id})

class Day(models.Model):
    number = models.IntegerField()  
    date = models.DateField(default='')
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    transport = models.CharField(
        max_length=1,
        choices = TRANSPORT,
        default = TRANSPORT[2][0]
    )
    lodging = models.CharField(max_length=50, default='')
    activities = models.ManyToManyField(Activity, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f'Day {self.number} of {self.trip}'
    
    def as_dict(self):
        return {
            'number' : self.number,
            'date' : self.date,
            'city' : self.city,
            'state' : self.state,
            'country' : self.country,
            'transport' : self.transport,
            'lodging' : self.lodging,
            'trip' : self.trip.id
        }
