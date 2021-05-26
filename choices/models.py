from django.db import models

# Choices/constraints/domains of database and django
 
class sensor_types(models.Model): #Nerc R25

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Sensor Types"

    def __str__(self): 
        return str(self.VALUE)

class sensor_makers(models.Model): 

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Sensor Makers"

    #Default return
    def __str__(self): 
        return str(self.DISPLAY)

class sensor_models(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Sensor Models"

    def __str__(self): 
        return str(self.VALUE)

class instrument_types(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Intrument Types"

    def __str__(self): 
        return str(self.DISPLAY)

class instrument_types_AOML(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "Intrument Types (AOML)"

    def __str__(self): 
        return str(self.DISPLAY)


class wmo_recorder_types(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000)
    
    class Meta:
        verbose_name_plural = "WMO Recorder Types"

    def __str__(self): 
        return str(self.DISPLAY)

class battery_types(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Battery Types"

    def __str__(self): 
        return str(self.DISPLAY)

class battery_manufacturers(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Battery Manufacturers"

    def __str__(self): 
        return str(self.DISPLAY)

class origin_countries(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Origin Countries"

    def __str__(self): 
        return str(self.DISPLAY)


class DeploymentType(models.TextChoices): #AOML, not Argo compliant
    RV = 'R/V','R/V'
    VOS = 'VOS','VOS'
    MV = 'M/V','M/V'
    AIR = 'AIR','AIR'

class deployment_platforms(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    TYPE = models.CharField(max_length=25, choices=DeploymentType.choices)
    NODC = models.CharField(max_length=25, blank=True, null=True)
    SOURCE = models.CharField(max_length=25, blank=True, null=True)
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Deployment Platforms"

    def __str__(self): 
        return str(self.DISPLAY)

class platform_makers(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Platform Makers"
    def __str__(self): 
        return str(self.DISPLAY)

class platform_types(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    KEY = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Platform Types"
    def __str__(self): 
        return str(self.DISPLAY)

class transmission_systems(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    SOURCE = models.CharField(max_length=50)
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Transmission Systems"
    def __str__(self): 
        return str(self.DISPLAY)

class institutions(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Institutions"
    def __str__(self): 
        return str(self.VALUE)

class funders(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Funders"
    def __str__(self): 
        return str(self.VALUE)

class events(models.Model):

    VALUE = models.CharField(max_length=100, unique=True)
    DISPLAY = models.CharField(max_length=200)
    ACTIVE = models.BooleanField()
    DESCRIPTION = models.CharField(max_length=2000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Events"
    def __str__(self): 
        return str(self.VALUE)