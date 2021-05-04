from django.db import models
from deployments.models import deployment
from choices.models import sensor_types, sensor_makers, sensor_models

# Fields of table
class sensor(models.Model): 

    DEPLOYMENT = models.ForeignKey(deployment, related_name='sensors', on_delete=models.CASCADE)

    ADD_DATE = models.DateTimeField() #creation of record in db
    SENSOR = models.ForeignKey(sensor_types, to_field="VALUE", max_length=50, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    SENSOR_MAKER = models.ForeignKey(sensor_makers, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    SENSOR_MODEL = models.ForeignKey(sensor_models, to_field="VALUE", max_length=50, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    SENSOR_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    SENSOR_CALIB_DATE = models.DateField(blank=True, null=True)
    PREDEPLOYMENT_CALIB_EQUATION = models.JSONField(max_length=100, blank=True, null=True)
    PREDEPLOYMENT_CALIB_COEFFICIENT =models.JSONField(max_length=100, blank=True, null=True)
    COMMENTS = models.TextField(blank=True, null=True)

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
        return translation[str(self.SENSOR)]

    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)