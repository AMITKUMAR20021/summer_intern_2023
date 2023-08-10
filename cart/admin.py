from django.contrib import admin
from .models import TemperatureReading, PulseReading, ECGReading

admin.site.register(TemperatureReading)
admin.site.register(PulseReading)
admin.site.register(ECGReading)
