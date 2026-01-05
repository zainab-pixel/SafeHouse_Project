from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/register/', views.api_register),
    path('api/login/', views.api_login),
    path('api/set_state/', views.set_state),       # Saves Logs
    path('api/sensor_input/', views.api_sensor_input), # Saves Sensors
    path('api/logs/', views.api_get_logs),         # Reads Logs
    path('api/sensors/', views.api_get_sensors),   # Reads Sensors
]