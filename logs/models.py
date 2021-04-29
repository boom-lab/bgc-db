from django.db import models
from deployments.models import deployment
from choices.models import events
from django.conf import settings

class Status(models.TextChoices):
    Success = 'Success','Success'
    Fail = 'Fail','Fail'
    Skip = 'Skip','Skip'

class file_processing(models.Model):

    DIRECTORY = models.CharField(max_length=200, unique=True)
    STATUS = models.CharField(max_length=200, choices=Status.choices)
    DETAILS = models.TextField(null=True, blank=True)
    DATE = models.DateTimeField() 
    
    class Meta:
        verbose_name_plural = "File Processing"

    def __str__(self): 
        return str(self.DIRECTORY)

class deployment_tracking(models.Model):

    DEPLOYMENT = models.ForeignKey(deployment, on_delete=models.CASCADE)
    EVENT = models.ForeignKey(events, to_field="VALUE", max_length=50, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    DATE = models.DateField()
    LOCATION = models.CharField(max_length=100, null=True, blank=True)
    COMMENT = models.TextField(null=True, blank=True)
    USER = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)


    
    class Meta:
        verbose_name_plural = "Deployment Tracking"

    def __str__(self): 
        return str(self.DEPLOYMENT)