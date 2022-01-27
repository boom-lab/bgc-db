from django.db import models
from sensors.models import sensor
from choices.models import qc_levels

# Fields of table
class sensor_qc(models.Model): 

    SENSOR = models.ForeignKey(sensor, related_name='sensor_qc', on_delete=models.CASCADE, limit_choices_to={'DEPLOYMENT__HISTORICAL':False})
    ADD_DATE = models.DateTimeField() #creation of record in db
    START_CYCLE = models.IntegerField("Start Cycle - Inclusive",null=True, blank=True)
    END_CYCLE = models.IntegerField("End Cycle - Inclusive", null=True, blank=True) 
    QC_LEVEL = models.ForeignKey(qc_levels, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT)
    PROBLEM = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sensor QC"
    #Default return
    def __str__(self): 
        return str(self.SENSOR)