from django.db import models

class Status(models.TextChoices):
    Success = 'Success','Success'
    Fail = 'Fail','Fail'

class file_processing(models.Model):

    DIRECTORY = models.CharField(max_length=200, unique=True)
    STATUS = models.CharField(max_length=200, choices=Status.choices)
    DETAILS = models.TextField(null=True, blank=True)
    DATE = models.DateTimeField() 
    
    class Meta:
        verbose_name_plural = "File Processing"

    def __str__(self): 
        return str(self.DIRECTORY)