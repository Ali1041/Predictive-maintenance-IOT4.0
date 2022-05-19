from django.contrib import admin
from .models import FeaturesObtained, SensorTwoData, SensorOneData
# Register your models here.

# admin.site.register(AccelerometerRawData)
admin.site.register(FeaturesObtained)
admin.site.register(SensorTwoData)
admin.site.register(SensorOneData)