from django.db import models

# Create your models here.

class AccelerometerRawData(models.Model):
    x_axis = models.CharField(blank=True, max_length=255)
    y_axis = models.CharField(blank=True, max_length=255)
    z_axis = models.CharField(blank=True, max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class FeaturesObtained(models.Model):
    mean = models.CharField(blank=True, max_length=255)
    std = models.CharField(blank=True, max_length=255)
    kurtosis = models.CharField(blank=True, max_length=255)
    skewness = models.CharField(blank=True, max_length=255)
    crest = models.CharField(blank=True, max_length=255)
    clearance = models.CharField(blank=True, max_length=255)
    shape = models.CharField(blank=True, max_length=255)
    impulse = models.CharField(blank=True, max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)