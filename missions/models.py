from django.db import models
from deployments.models import deployment

# Fields of table
class mission(models.Model): 
    DEPLOYMENT = models.ForeignKey(deployment, related_name='missions', on_delete=models.DO_NOTHING)

    ADD_DATE = models.DateTimeField() #creation of record in db

    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)