from django.db import models

# 1. USERS (For Login and Registration)
class AppUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='user')
    permissions = models.CharField(max_length=500, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# 2. LOGS (Web history)
class EventLog(models.Model):
    device_id = models.CharField(max_length=50) # ex: "kitchen-light"
    action = models.CharField(max_length=100)   # ex: "Turned ON"
    user_email = models.CharField(max_length=100, default="System") 
    timestamp = models.DateTimeField(auto_now_add=True)

# 3. SENSORS (Data received every minute)
class SensorData(models.Model):
    sensor_type = models.CharField(max_length=50) # ex: "Temperature"
    value = models.FloatField()
    unit = models.CharField(max_length=10) # ex: "°C"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_type}: {self.value}"