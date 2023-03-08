from django.db import models
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
    days = models.IntegerField()
    start = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Trip to {self.name} on {self.start}'

class Day(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    transport = models.CharField(
        max_length=1,
        choices = TRANSPORT,
        default = TRANSPORT[2][1]
    )
    lodging = models.CharField(max_length=50)
    activities = models.ManyToManyField(Activity)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f'Day {self.number} of {self.trip}'





