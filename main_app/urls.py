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

    # Activities
    path('days/<int:day_id>/activity_create', views.activity_create, name='activity_create'),
    path('activity/<int:pk>/update', views.ActivityUpdate.as_view(), name='activity_update'),
    path('days/<int:day_id>/delete/<int:activity_id>/', views.activity_delete, name='activity_delete'),
    path('activity/<int:activity_id>', views.activity_detail, name='activity_detail'),
    
    # Auth
    path('accounts/signup/', views.signup, name='signup'),

    # Photos
    path('trips/<int:trip_id>/add_photo', views.add_photo, name='add_photo')
    
]