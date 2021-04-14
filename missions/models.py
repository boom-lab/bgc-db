from django.db import models
from deployments.models import deployment

# Fields of table
class mission(models.Model): 
    DEPLOYMENT = models.ForeignKey(deployment, related_name='missions', on_delete=models.DO_NOTHING)
    ADD_DATE = models.DateTimeField() #creation of record in db

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

    COMMENTS = models.TextField(blank=True, null=True)
    
    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)