from django.db import models
from choices.models import platform_makers, platform_types, transmission_systems, instrument_types, institutions, funders

#Domains for choices and db contstraints
class Status(models.TextChoices): #AOML, not Argo compliant
    ESTIMATED = 'estimated','estimated'
    AS_RECORDED = 'as recorded','as recorded'
    UNKNOWN = 'unknown','unknown'

class DeploymentType(models.TextChoices): #AOML, not Argo compliant
    RV = 'R/V','R/V'
    VOS = 'VOS','VOS'
    MV = 'M/V','M/V'
    AIR = 'AIR','AIR'

class deployment(models.Model):
    # fields of the database
    ADD_DATE = models.DateTimeField() #creation of record in db
    AOML_ID = models.CharField(max_length=25, blank=True, null=True)
    PLATFORM_NUMBER = models.CharField("PLATFORM NUMBER (WMO)", max_length=25, unique=True, blank=True, null=True) #WMO
    FLOAT_SERIAL_NO = models.IntegerField(blank=True, null=True)
    PLATFORM_MAKER = models.ForeignKey(platform_makers, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    PLATFORM_TYPE = models.ForeignKey(platform_types, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    INST_TYPE = models.CharField(max_length=25, blank=True, null=True)
    WMO_INST_TYPE = models.ForeignKey(instrument_types, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    WMO_RECORDER_TYPE = models.CharField(max_length=25, blank=True, null=True)

    TRANS_SYSTEM = models.ForeignKey(transmission_systems, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    IRIDIUM_PROGRAM_NO = models.CharField(max_length=25, blank=True, null=True)

    START_DATE = models.DateTimeField(blank=True, null=True)
    START_DATE_QC = models.CharField(max_length=25, choices=Status.choices, default=Status.ESTIMATED, blank=True, null=True)
    
    LAUNCH_DATE = models.DateTimeField(blank=True, null=True)
    LAUNCH_DATE_QC = models.CharField(max_length=25, choices=Status.choices, default=Status.ESTIMATED, blank=True, null=True)
    LAUNCH_LATITUDE = models.FloatField(blank=True, null=True) #WGS84 decimal degrees
    LAUNCH_LONGITUDE = models.FloatField(blank=True, null=True) #WGS84 decimal degrees
    LAUNCH_POSITION_QC = models.CharField(max_length=25, choices=Status.choices, default=Status.ESTIMATED, blank=True, null=True)

    INSTITUTION = models.ForeignKey(institutions, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    FUNDER = models.ForeignKey(funders, to_field="VALUE", max_length=25, blank=True, null=True, on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    PI_NAME  = models.CharField(max_length=100, blank=True, null=True)
    PI_ADDRESS = models.CharField(max_length=100, blank=True, null=True)
    ORIGIN_COUNTRY = models.CharField(max_length=25, blank=True, null=True)

    DEPLOYER = models.CharField(max_length=25, blank=True, null=True)
    DEPLOYER_ADDRESS = models.CharField(max_length=100, blank=True, null=True)
    DEPLOYMENT_TYPE = models.CharField(choices=DeploymentType.choices, max_length=25, blank=True, null=True)
    DEPLOYMENT_PLATFORM = models.CharField(max_length=25, blank=True, null=True)
    DEPLOYMENT_CRUISE_ID = models.CharField(max_length=25, blank=True, null=True)
    DEPLOYMENT_REFERENCE_STATION_ID = models.CharField(max_length=25, blank=True, null=True)
    DEPLOYMENT_PLATFORM_ID = models.CharField(max_length=25, blank=True, null=True)
    
    FLOAT_CONTROLLER_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    LBT_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    GPS_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    ROM_VERSION = models.CharField(max_length=25, blank=True, null=True)

    BATTERY_TYPE = models.CharField(max_length=25, blank=True, null=True)
    BATTERY_MANUFACTURER = models.CharField(max_length=25, blank=True, null=True)
    BATTERY_MODEL = models.CharField(max_length=25, blank=True, null=True)
    BATTERY_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    BATTERY_VOLTAGE = models.FloatField(max_length=25, blank=True, null=True)
    BATTERY_PACKS = models.CharField(max_length=25, blank=True, null=True)
    BATTERY_DETAILS = models.CharField(max_length=25, blank=True, null=True)
    PUMP_BATTERY_SERIAL_NO = models.IntegerField(blank=True, null=True)

    CUSTOMIZATION = models.CharField(max_length=200, blank=True, null=True)
    COMMENTS = models.TextField(blank=True, null=True)

    #For admin detail view
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    # renames the instances of the model 
    # with their title name 
    def __str__(self): 
        return 'SN: '+str(self.FLOAT_SERIAL_NO)+' ID: '+str(self.id) + " WMO: " + str(self.PLATFORM_NUMBER)