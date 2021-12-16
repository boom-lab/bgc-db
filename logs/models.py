from django.db import models
from deployments.models import deployment
from choices.models import events
from choices.models import tracking_error_types
from django.conf import settings

class Status(models.TextChoices):
    Success = 'Success','Success'
    Fail = 'Fail','Fail'
    Warning = 'Warning','Warning'
    Skip = 'Skip','Skip'
    Reprocess = 'Reprocess','Reprocess'

class file_processing(models.Model):

    DIRECTORY = models.CharField(max_length=200, unique=True)
    FLOAT_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    CYCLE = models.CharField(max_length=3, blank=True, null=True)
    STATUS = models.CharField(max_length=200, choices=Status.choices)
    DETAILS = models.TextField(null=True, blank=True)
    DATE = models.DateTimeField() 

    class Meta:
        verbose_name_plural = "File Processing"

    def __str__(self): 
        return str(self.DIRECTORY)

class deployment_tracking(models.Model):

    DEPLOYMENT = models.ForeignKey(deployment, on_delete=models.CASCADE, related_name='deployment_tracking')
    EVENT = models.ForeignKey(events, to_field="VALUE", max_length=50, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    DATE = models.DateField()
    ERROR_TYPE = models.ForeignKey(tracking_error_types, on_delete=models.PROTECT, null=True, blank=True)
    LOCATION = models.CharField(max_length=100, null=True, blank=True)
    COMMENT = models.TextField(null=True, blank=True)
    USER = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)


    
    class Meta:
        verbose_name_plural = "Deployment Tracking"
        ordering = ["-DATE"]

    def __str__(self): 
        return str(self.DEPLOYMENT)