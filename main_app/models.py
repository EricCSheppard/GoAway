from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django import forms


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

INOUT = (
    ('I', 'Inside'),
    ('O', 'Outside')
)

class Activity(models.Model):
    name = models.CharField(max_length=50)
    time = models.TimeField()
    inout = models.CharField(
        max_length = 1,
        choices = INOUT,
        default = INOUT[0][0]
    )
    description = models.CharField(max_length=125)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('day', kwargs={'activity_id': self.id})
    

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
    state = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='')
    transport = models.CharField(
        max_length=1,
        choices = TRANSPORT,
        default = TRANSPORT[2][0],
        blank=True
    )
    lodging = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=70, default='')
    flight = models.CharField(max_length=20, default='', blank=True)
    activities = models.ManyToManyField(Activity, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Day {self.number} of {self.trip}'
    
    def as_dict(self):
        return {
            'number' : self.number,
            'date' : self.date
            # 'city' : self.city,
            # 'state' : self.state,
            # 'country' : self.country,
            # 'transport' : self.transport,
            # 'lodging' : self.lodging,
            # 'trip' : self.trip.id
        }
    def get_absolute_url(self):
        return reverse('day_detail', kwargs={'day_id': self.id})