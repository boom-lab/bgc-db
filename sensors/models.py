from django.db import models
from deployments.models import deployment
from choices.views import get_choices

class Sensors(models.TextChoices):
    test = 'test','test'


Sensor_Choices = get_choices('sensor_types')
Maker_Choices = get_choices('sensor_makers')
Model_Choices = get_choices('sensor_models')

# Fields of table
class sensor(models.Model): 

    DEPLOYMENT = models.ForeignKey(deployment, related_name='sensors', on_delete=models.CASCADE)

    ADD_DATE = models.DateTimeField() #creation of record in db
    SENSOR = models.CharField(choices=Sensor_Choices, max_length=50)
    SENSOR_MAKER = models.CharField(choices=Maker_Choices, max_length=25, blank=True, null=True)
    SENSOR_MODEL = models.CharField(choices=Model_Choices, max_length=25, blank=True, null=True)
    SENSOR_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    SENSOR_CALIB_DATE = models.DateField(blank=True, null=True)
    PREDEPLOYMENT_CALIB_EQUATION = models.JSONField(max_length=100, blank=True, null=True)
    PREDEPLOYMENT_CALIB_COEFFICIENT =models.JSONField(max_length=100, blank=True, null=True)
    COMMENTS = models.TextField(blank=True, null=True)

    #Database constraints
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_SENSOR_CHECKS",
                check=models.Q(SENSOR__in=[pair[0] for pair in Sensor_Choices])
                & models.Q(SENSOR_MAKER__in=[pair[0] for pair in Maker_Choices])
                & models.Q(SENSOR_MODEL__in=[pair[0] for pair in Model_Choices])
            )
        ]

    #For aoml metadata template, converts SENSOR into their text format
    def aoml_sensor(self):
        translation = {'PUMP_VOLTAGE':'pump voltage',
            'CPU_VOLTAGE':'cpu voltage',
            'FLUOROMETER_CHLA':'fluoro CHLA',
            'BACKSCATTERINGMETER_BBP700':'fluoro BBP700',
            'SPECTROPHOTOMETER_NITRATE':'nitrate',
            'CTD_CNDC':'conductivity',
            'TRANSISTOR_PH':'ph',
            'FLUOROMETER_CDOM':'fluoro CDOM',
            'RADIOMETER_PAR':'par',
            'CTD_TEMP':'temperature',
            'OPTODE_DOXY':'oxygen',
            'CTD_PRES':'pressure',
            'SPECTROPHOTOMETER_NITRATE':'nitrate'}
        return translation[self.SENSOR]

    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)