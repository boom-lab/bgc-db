from datetime import datetime, timezone, timedelta
from django.db import models
from choices.models import platform_makers, platform_types, transmission_systems, instrument_types, institutions, funders
import numpy as np

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

class ModemType(models.TextChoices): #internal, not argo compliant
    Civilian = 'Civilian','Civilian'
    DOD = 'DOD','Department of Defence'

class deployment(models.Model):
    # fields of the database
    ADD_DATE = models.DateTimeField() #creation of record in db
    AOML_ID = models.CharField(max_length=25, blank=True, null=True)
    PLATFORM_NUMBER = models.CharField("PLATFORM NUMBER (WMO)", max_length=25, unique=True, blank=True, null=True) #WMO
    FLOAT_SERIAL_NO = models.IntegerField(blank=True, null=True)
    DEATH_DATE = models.DateTimeField(blank=True, null=True)
    WHOI_TAG = models.CharField(max_length=25, blank=True, null=True)
    PURCHACE_ORDER = models.CharField(max_length=25, blank=True, null=True)
    PLATFORM_MAKER = models.ForeignKey(platform_makers, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    PLATFORM_TYPE = models.ForeignKey(platform_types, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    INST_TYPE = models.CharField(max_length=25, blank=True, null=True)
    WMO_INST_TYPE = models.ForeignKey(instrument_types, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    WMO_RECORDER_TYPE = models.CharField(max_length=25, blank=True, null=True)

    TRANS_SYSTEM = models.ForeignKey(transmission_systems, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    IRIDIUM_PROGRAM_NO = models.CharField(max_length=25, blank=True, null=True)
    MODEM_TYPE = models.CharField(choices=ModemType.choices, max_length=25, blank=True, null=True)
    MODEM_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)

    START_DATE = models.DateTimeField(blank=True, null=True)
    START_DATE_QC = models.CharField(max_length=25, choices=Status.choices, default=Status.ESTIMATED, blank=True, null=True)
    
    LAUNCH_DATE = models.DateTimeField(blank=True, null=True)
    LAUNCH_DATE_QC = models.CharField(max_length=25, choices=Status.choices, default=Status.ESTIMATED, blank=True, null=True)
    LAUNCH_LATITUDE = models.FloatField(blank=True, null=True) #WGS84 decimal degrees
    LAUNCH_LONGITUDE = models.FloatField(blank=True, null=True) #WGS84 decimal degrees
    LAUNCH_POSITION_QC = models.CharField(max_length=25, choices=Status.choices, default=Status.ESTIMATED, blank=True, null=True)

    INSTITUTION = models.ForeignKey(institutions, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    FUNDER = models.ForeignKey(funders, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
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
    DEPLOYMENT_EXPECTED_MOB = models.DateTimeField(blank=True, null=True)
    
    FLOAT_CONTROLLER_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
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

    @property
    def last_report(self):
        latest = self.cycle_metadata.order_by('-DATE_ADD').first()
        if latest: 
            return latest.TimeStartTelemetry
        return None

    @property
    def status(self):
        if not self.LAUNCH_DATE: #Before launch
            return "Predeployment"
        latest = self.cycle_metadata.order_by('-DATE_ADD').first()
        if latest.PROFILE_ID[-3:] == '000': #first .msg file reported
            return "Prelude"
        if datetime.now(timezone.utc)-self.last_report > timedelta(days = 10): #Most recent report is older than 10 days
            return "Overdue"
        return "Active"

    @property
    def next_report(self):
        """Estimates the next report date by averaging the past five cycles (or less than 5 if there are less than 5 reports)"""
        n_reports = self.cycle_metadata.count()
        if n_reports <2:
            return None
        else:
            if n_reports < 5:
                n_mean = n_reports
            else:
                n_mean = 5

            query = self.cycle_metadata.order_by('-GpsFixDate').all()[0:n_mean]
            recent_reports = np.array(query.values_list('GpsFixDate', flat=True))
            time_diff = (np.diff(np.flip(recent_reports, axis=0)))
            mean_time_diff = np.mean(time_diff)

            return recent_reports[0] + mean_time_diff

    @property
    def age(self):
        n_reports = self.cycle_metadata.count()
        if n_reports == 0:
            return None
        if self.DEATH_DATE:
            return self.DEATH_DATE - self.LAUNCH_DATE
        return datetime.now(timezone.utc) - self.LAUNCH_DATE

    #For admin detail view
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    # renames the instances of the model 
    # with their title name 
    def __str__(self): 
        return 'SN: '+str(self.FLOAT_SERIAL_NO)+' ID: '+str(self.id) + " WMO: " + str(self.PLATFORM_NUMBER)