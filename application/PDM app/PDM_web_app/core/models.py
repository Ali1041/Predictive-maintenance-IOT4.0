from django.db import models

# Create your models here.

CHOICES = (
    ('S1B1', 'S1B1'),
    ('S1B2', 'S1B2'),
    ('S2B1', 'S2B1'),
    ('S2B2', 'S2B2')
)

class SensorOneData(models.Model):
    x_axis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    y_axis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    z_axis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.created_at} x:{self.x_axis}, y:{self.y_axis}'

class SensorTwoData(models.Model):
    x_axis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    y_axis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    z_axis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return f'{self.created_at} x:{self.x_axis}, y:{self.y_axis}'


class FeaturesObtained(models.Model):
    name = models.CharField(blank=True, max_length=255, choices=CHOICES)
    axis = models.CharField(blank=True, max_length=255, choices=(('x','x'),('y','y')))
    mean = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    std = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    kurtosis = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    skewness = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    crest = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    clearance = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    shape = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    impulse = models.DecimalField(blank=True,null=True, decimal_places=8,max_digits=12 )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)