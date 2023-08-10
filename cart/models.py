from django.db import models

class TemperatureReading(models.Model):
    temperature = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

class PulseReading(models.Model):
    pulse = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

class ECGReading(models.Model):
    ecg_data = models.TextField()
    time = models.DateTimeField(auto_now_add=True)