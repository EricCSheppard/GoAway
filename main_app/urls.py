from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Trips
    path('trips/', views.trip_index, name='trip_index'),
    path('trips/create/', views.TripCreate.as_view(), name='trip_create'),
    path('trips/<int:pk>/delete/', views.TripDelete.as_view(), name='trip_delete'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),

    #  Days
    path('days/create/<int:trip_id>', views.days_create, name='days_create'),
    path('days/populate/<int:trip_id>', views.days_populate, name='days_populate' ),
    path('days/<int:pk>/update/', views.DayUpdate.as_view(), name='day_update'),
    path('days/<int:day_id>/', views.day_detail, name='day_detail'),
    
]