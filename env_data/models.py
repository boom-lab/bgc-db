from django.db import models
from deployments.models import deployment

class profile_metadata(models.Model):

    #fields of the model
    DEPLOYMENT = models.ForeignKey(deployment, related_name='profile_metadata', on_delete=models.DO_NOTHING)
    
    DATE_ADD = models.DateTimeField() #creation of record in db
    PROFILE_ID = models.CharField(default=0, blank=True, null=True, max_length=20, unique=True)

    #Default return
    def __str__(self): 
        return str(self.PROFILE_ID)


meta_int_fields = ['ActiveBallastAdjustments', 'AirBladderPressure', 'AirPumpAmps', 'AirPumpVolts', 'BatteryCounts', 
    'BuoyancyPumpOnTime', 'BuoyancyPumpAmps', 'BuoyancyPumpVolts', 'CurrentBuoyancyPosition', 'DeepProfileBuoyancyPosition', 'FlashErrorsCorrectable', 
    'FlashErrorsUncorrectable', 'FloatId', 'GpsFixTime',  'IceMLSample', 'McomsAmps', 'McomsVolts', 'Ocr504Amps', 
    'Ocr504Volts', 'ParkDescentPCnt', 'ParkBuoyancyPosition', 'ProfileId', 'ObsIndex', 'QuiescentAmps', 'QuiescentVolts', 'Sbe41cpAmps', 'Sbe41cpVolts', 
       'Sbe63Amps', 'Sbe63Volts',  'SurfaceBuoyancyPosition', 
     'Vacuum']
meta_str_fields = ['NpfFwRev', 'IceEvasionRecord', 'IceMLMedianT','Sbe41cpStatus', 'status',]
meta_float_fields = ['gps_lon', 'gps_lat','Sbe41cpHumidity','Sbe41cpHumidityTemp','SurfacePressure', ]
meta_date_fields = ['TimeStartDescent', 'TimeStartPark', 'TimeStartProfileDescent', 'TimeStartProfile', 'TimeStopProfile', 'TimeStartTelemetry']

for field in meta_int_fields:
    profile_metadata.add_to_class(field, models.IntegerField(blank=True, null=True))

for field in meta_str_fields:
    profile_metadata.add_to_class(field, models.CharField(blank=True, null=True, max_length=50))

for field in meta_float_fields:
    profile_metadata.add_to_class(field, models.FloatField(blank=True, null=True))

for field in meta_date_fields:
    profile_metadata.add_to_class(field, models.DateTimeField(blank=True, null=True))



class mission_reported(models.Model):
    DEPLOYMENT = models.ForeignKey(deployment, related_name='mission_reported', on_delete=models.DO_NOTHING)
    DATE_ADD = models.DateTimeField() #creation of record in db
    PROFILE_ID = models.CharField(default=0, blank=True, null=True, max_length=20, unique=True)
    
    AscentTimeOut = models.IntegerField(blank=True, null=True)
    BuoyancyNudge = models.IntegerField(blank=True, null=True)
    BuoyancyNudgeInitial = models.IntegerField(blank=True, null=True)
    ConnectTimeOut = models.IntegerField(blank=True, null=True)
    CpActivationP = models.IntegerField(blank=True, null=True)
    DeepProfileDescentTime = models.IntegerField(blank=True, null=True)
    DeepProfileBuoyancyPos = models.IntegerField(blank=True, null=True)
    DeepProfilePressure = models.IntegerField(blank=True, null=True)
    DownTime = models.IntegerField(blank=True, null=True)
    FloatId = models.CharField(max_length=25, blank=True, null=True)
    FullExtension = models.IntegerField(blank=True, null=True)
    FullRetraction = models.IntegerField(blank=True, null=True)
    IceDetectionP = models.FloatField(blank=True, null=True)
    IceEvasionP = models.FloatField(blank=True, null=True)
    IceMLTCritical = models.FloatField(blank=True, null=True)
    IceMonths = models.CharField(max_length=25, blank=True, null=True)
    IsusInit = models.IntegerField(blank=True, null=True)
    HpvEmfK = models.FloatField(blank=True, null=True)
    HpvRes = models.IntegerField(blank=True, null=True)
    MaxAirBladder = models.IntegerField(blank=True, null=True)
    MaxLogKb = models.IntegerField(blank=True, null=True)
    MissionPrelude = models.IntegerField(blank=True, null=True)
    OkVacuum = models.IntegerField(blank=True, null=True)
    PActivationBuoyancyPosition = models.IntegerField(blank=True, null=True)
    ParkDescentTime = models.IntegerField(blank=True, null=True)
    ParkBuoyancyPos = models.IntegerField(blank=True, null=True)
    ParkPressure = models.IntegerField(blank=True, null=True)
    PnPCycleLen = models.IntegerField(blank=True, null=True)
    TelemetryRetry = models.IntegerField(blank=True, null=True)
    TimeOfDay = models.IntegerField(blank=True, null=True)
    UpTime = models.IntegerField(blank=True, null=True)
    PhBattMode = models.IntegerField(blank=True, null=True)
    Verbosity = models.IntegerField(blank=True, null=True)
    DebugBits = models.CharField(max_length=25, blank=True, null=True)

    #Default return
    def __str__(self): 
        return str(self.PROFILE_ID)

# Tabe in db
class profile(models.Model):

    #fields of the model
    DEPLOYMENT = models.ForeignKey(deployment, on_delete=models.DO_NOTHING)
    PROFILE_METADATA = models.ForeignKey(profile_metadata, to_field='PROFILE_ID', on_delete=models.DO_NOTHING)
    
    
    DATE_ADD = models.DateTimeField() #creation of record in db
    MISSION = models.ForeignKey(mission_reported, to_field='PROFILE_ID', on_delete=models.DO_NOTHING)
    
    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)


profile_fields = ['PRES', 'TEMP', 'PSAL', 'NCTD', 'OPH', 'OTV', 'NO', 'MCH1', 'MCH2', 'MCH3', 'NM', 'OCR1', 'OCR2', 'OCR3', 'OCR4', 'NI', 
'IN', 'AZ', 'SA', 'CT', 'SIGMA0', 'Z', 'DOXY', 'CHLA', 'BBP700', 'CDOM', 'WN_IRR380', 'WN_IRR412', 'WN_IRR490', 'PAR']

for field in profile_fields:
    profile.add_to_class(field, models.FloatField(blank=True, null=True))



# Table in db
class park(models.Model):

    #fields of the model
    DEPLOYMENT = models.ForeignKey(deployment, related_name='park', on_delete=models.DO_NOTHING)
    DATE_ADD = models.DateTimeField()
    DATE_MEASURED = models.DateTimeField()
    PRES = models.FloatField() #Blank=True is not required
    TEMP = models.FloatField()
    PSAL = models.FloatField()
    OPH = models.FloatField()
    OTV = models.FloatField()

    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)