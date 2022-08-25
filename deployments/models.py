from datetime import datetime, timezone, timedelta
from django.db import models
from choices.models import platform_makers, transmission_systems, institutions, funders
from choices import models as cm
import numpy as np

#Domains for choices and db contstraints
class Status(models.TextChoices): #AOML, not Argo compliant
    ESTIMATED = 'estimated','estimated'
    AS_RECORDED = 'as recorded','as recorded'
    UNKNOWN = 'unknown','unknown'

class ModemType(models.TextChoices): #internal, not argo compliant
    Civilian = 'Civilian','Civilian'
    DOD = 'DOD','Department of Defence'

class deployment(models.Model):
    # fields of the database
    PROCESSING_ACTIVE = models.BooleanField(default=False)
    ADD_DATE = models.DateTimeField() #creation of record in db
    AOML_ID = models.CharField(max_length=25, blank=True, null=True)
    PLATFORM_NUMBER = models.CharField("PLATFORM NUMBER (WMO)", max_length=25, unique=True, blank=True, null=True) #WMO
    FLOAT_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    DEATH_DATE = models.DateTimeField(blank=True, null=True)
    WHOI_TAG = models.CharField(max_length=25, blank=True, null=True)
    PURCHASE_ORDER = models.CharField(max_length=25, blank=True, null=True)
    PLATFORM_MAKER = models.ForeignKey(platform_makers, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    PLATFORM_TYPE = models.ForeignKey(cm.platform_types, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True}) #R23
    PLATFORM_TYPE_AOML = models.ForeignKey(cm.platform_types_aoml, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True}) 
    PLATFORM_TYPE_WMO = models.ForeignKey(cm.platform_types_wmo, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True}) #R08
    WMO_RECORDER_TYPE = models.ForeignKey(cm.wmo_recorder_types, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})

    DRY_WEIGHT = models.FloatField("DRY WEIGHT (g)", blank=True, null=True)
    
    TRANS_SYSTEM = models.ForeignKey(transmission_systems, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    MODEM_TYPE = models.CharField(choices=ModemType.choices, max_length=25, blank=True, null=True)
    MODEM_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    IMEI = models.CharField(max_length=15, blank=True, null=True)
    SIM = models.CharField(max_length=19, blank=True, null=True)

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
    ORIGIN_COUNTRY = models.ForeignKey(cm.origin_countries, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})

    DEPLOYER = models.CharField(max_length=100, blank=True, null=True)
    DEPLOYER_ADDRESS = models.CharField(max_length=100, blank=True, null=True)
    DEPLOYMENT_PLATFORM = models.ForeignKey(cm.deployment_platforms, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    DEPLOYMENT_CRUISE_ID = models.CharField(max_length=50, blank=True, null=True)
    DEPLOYMENT_REFERENCE_STATION_ID = models.CharField(max_length=50, blank=True, null=True)
    DEPLOYMENT_MOB = models.DateField(blank=True, null=True)
    DEPLOYMENT_PORT = models.CharField(max_length=50, blank=True, null=True)
    
    FLOAT_CONTROLLER_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    GPS_SERIAL_NO = models.CharField(max_length=25, blank=True, null=True)
    ROM_VERSION = models.CharField(max_length=25, blank=True, null=True)

    BATTERY_TYPE = models.ForeignKey(cm.battery_types, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    BATTERY_MANUFACTURER = models.ForeignKey(cm.battery_manufacturers, to_field="VALUE", max_length=25, blank=True, null=True, 
        on_delete=models.PROTECT, limit_choices_to={'ACTIVE':True})
    BATTERY_MODEL = models.CharField(max_length=25, blank=True, null=True)
    BATTERY_SERIAL_NO = models.CharField(max_length=50, blank=True, null=True)
    BATTERY_VOLTAGE = models.FloatField(max_length=25, blank=True, null=True)
    BATTERY_PACKS = models.CharField(max_length=50, blank=True, null=True)
    BATTERY_DETAILS = models.CharField(max_length=100, blank=True, null=True)
    PUMP_BATTERY_SERIAL_NO = models.CharField(max_length=50, blank=True, null=True)

    NOMINAL_DRIFT_PRES = models.IntegerField(null=True, blank=True)
    CYCLES_FOR_DRIFT_PRES = models.IntegerField(null=True, blank=True)
    NOMINAL_PROFILE_PRES = models.IntegerField(null=True, blank=True)
    CYCLES_FOR_PROFILE_PRES = models.IntegerField(null=True, blank=True)
    PROFILE_SAMPLING_METHOD = models.CharField(max_length=200, blank=True, null=True)
    PROFILE_SAMPLING_METHOD_2 = models.CharField(max_length=200, blank=True, null=True)

    CUSTOMIZATION = models.CharField(max_length=200, blank=True, null=True)
    COMMENTS = models.TextField(blank=True, null=True)
    HISTORICAL = models.BooleanField(default=False)

    @property
    def last_event(self):
        latest = self.deployment_tracking.order_by("DATE","id").last()
        if latest: 
            return {'EVENT':latest.EVENT,'COMMENT':latest.COMMENT,'LOCATION':latest.LOCATION}
        return None

    @property
    def last_location(self):
        latest = self.deployment_tracking.order_by("DATE").last()
        if latest: 
            return latest.LOCATION
        return None

    @property
    def last_report(self):
        latest = self.cycle_metadata.order_by('GpsFixDate').last()
        if latest: 
            return latest.GpsFixDate
        return None

    @property
    def last_cycle(self):
        latest = self.cycle_metadata.order_by('GpsFixDate').last()
        if latest: 
            return latest.ProfileId
        return None

    @property
    def incoming_status(self):
        events = list(self.deployment_tracking.order_by("DATE","id").values_list('EVENT', flat=True))
        if "RETURNED" in events:
            return_indx = len(events) - events[::-1].index('RETURNED') #Index of last occurance of "RETURNED" in list +1
            events = events[return_indx:]

        if 'PASSED_INCOMING' in events:
            return u'\u2713'
        return ''

    @property
    def internal_inspection_status(self):
        events = list(self.deployment_tracking.order_by("DATE","id").values_list('EVENT', flat=True))
        if "RETURNED" in events:
            events = events[events.index('RETURNED')+1:]
        if 'PASSED_INTERNAL_INSPECTION' in events:
            return u'\u2713'
        return ''

    @property
    def docktest_status(self):
        events = list(self.deployment_tracking.order_by("DATE","id").values_list('EVENT', flat=True))
        if "RETURNED" in events:
            events = events[events.index('RETURNED')+1:]
        if 'PASSED_DOCKTEST' in events:
            return u'\u2713'
        return ''

    @property
    def pressure_test_status(self):
        events = list(self.deployment_tracking.order_by("DATE","id").values_list('EVENT', flat=True))
        if "RETURNED" in events:
            events = events[events.index('RETURNED')+1:]
        if 'PASSED_PRESSURE_TEST' in events:
            return u'\u2713'
        return ''

    @property
    def flow_through_status(self):
        events = list(self.deployment_tracking.order_by("DATE","id").values_list('EVENT', flat=True))
        if "RETURNED" in events:
            events = events[events.index('RETURNED')+1:]
        if "FAILED_FLOW_THROUGH" in events:
            events = events[events.index('FAILED_FLOW_THROUGH')+1:]
        if 'PASSED_FLOW_THROUGH' in events:
            return u'\u2713'
        return ''


    @property
    def status(self):
        if not self.LAUNCH_DATE: #Before launch
            return "Predeployment"
        latest = self.cycle_metadata.order_by('GpsFixDate').last() #Historical floats
        if not latest:
            return ""
        if latest.PROFILE_ID[-3:] == '000': #first .msg file reported
            return "Prelude"
        if datetime.now(timezone.utc)-self.last_report > timedelta(days = 11): #Most recent report is older than 11 days
            return "Overdue"
        return "Active"

    @property
    def next_report(self):
        """Estimates the next report date by averaging the past 3 cycles (or less than 3 if there are less than 3 reports)"""
        n_reports = self.cycle_metadata.count()
        if n_reports <2:
            return None
        if n_reports < 3:
            n_mean = n_reports
        else:
            n_mean = 3

        query = self.cycle_metadata.order_by('-GpsFixDate').all()[0:n_mean]
        recent_reports = np.array(query.values_list('GpsFixDate', flat=True))
        time_diff = (np.diff(np.flip(recent_reports, axis=0)))
        mean_time_diff = np.mean(time_diff)

        return recent_reports[0] + mean_time_diff

    @property
    def days_since_last(self):
        """Days since last report"""
        latest = self.cycle_metadata.order_by('GpsFixDate').last()
        if latest:
            since_last = datetime.now(timezone.utc)-latest.GpsFixDate
            return since_last.days
        return ''

    @property
    def age(self):
        """Age of float"""
        n_reports = self.cycle_metadata.count()
        if n_reports == 0:
            return timedelta(days=0)
        if self.DEATH_DATE:
            return self.DEATH_DATE - self.LAUNCH_DATE
        return datetime.now(timezone.utc) - self.LAUNCH_DATE

    @property
    def sorted_sensors(self):
        return self.sensors.order_by('SENSOR')

    #For admin detail view
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    # renames the instances of the model 
    # with their title name 
    def __str__(self): 
        return 'SN: '+str(self.FLOAT_SERIAL_NO)+' ID: '+str(self.id) + " WMO: " + str(self.PLATFORM_NUMBER)