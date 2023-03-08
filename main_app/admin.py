from django.contrib import admin

from .models import Trip, Day, Activity

# Register your models here.
admin.site.register(Trip)
admin.site.register(Day)
admin.site.register(Activity)