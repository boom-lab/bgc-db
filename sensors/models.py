from django.db import models
from deployments.models import deployment

class Sensors(models.TextChoices): #Nerc R10
    CTD_PRES = 'CTD_PRES','CTD_PRES'
    CTD_TEMP = 'CTD_TEMP','CTD_TEMP'
    CTD_CNDC = 'CTD_CNDC', 'CTD_CNDC'
    IDO_DOXY = 'IDO_DOXY','IDO_DOXY'
    OPTODE_DOXY = 'OPTODE_DOXY','OPTODE_DOXY'

class Makers(models.TextChoices): #Nerc R26
    AANDERAA = 'AANDERAA','AANDERAA'
    AMETEK = 'AMETEK','AMETEK'
    SATLANTIC = 'SATLANTIC','SATLANTIC'
    SBE = 'SEB', 'SBE'
    WETLABS = 'WETLABS','WETLABS'

class Models(models.TextChoices): #Nerc R27
    SBE41CP = 'SBE41CP','SBE41CP'
    
# Fields of table
class sensor(models.Model): 

    DEPLOYMENT = models.ForeignKey(deployment, related_name='sensors', on_delete=models.DO_NOTHING)

    ADD_DATE = models.DateTimeField() #creation of record in db
    SENSOR = models.CharField(choices=Sensors.choices, max_length=25, blank=True, null=True)
    SENSOR_MAKER = models.CharField(choices=Makers.choices, max_length=25, blank=True, null=True)
    SENSOR_MODEL = models.CharField(choices=Models.choices, max_length=25, blank=True, null=True)
    SENSOR_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    PREDEPLOYMENT_CALIB_EQUATION = models.CharField(max_length=100, blank=True, null=True)
    PREDEPLOYMENT_CALIB_COEFFICIENT =models.CharField(max_length=100, blank=True, null=True)

    #Database constraints
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_SENSOR_CHECKS",
                check=models.Q(SENSOR__in=Sensors.values)
                & models.Q(SENSOR_MAKER__in=Makers.values)
                & models.Q(SENSOR_MODEL__in=Models.values)
            )
        ]

    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)