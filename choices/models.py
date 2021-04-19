from django.db import models

# Choices/constraints/domains of database and django
 
class sensor_types(models.Model): #Nerc R25

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Sensor Types"

class sensor_makers(models.Model): 

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Sensor Makers"

class sensor_models(models.Model):

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Sensor Models"


class instrument_types(models.Model):

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Intrument Types"


class platform_makers(models.Model):

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Platform Makers"


class platform_types(models.Model):

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    KEY = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Platform Types"


class transmission_systems(models.Model):

    VALUE = models.CharField(max_length=100)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Transmission Systems"