from django.db import models
from deployments.models import deployment

# Fields of table
class mission(models.Model): 
    DEPLOYMENT = models.ForeignKey(deployment, related_name='missions', on_delete=models.CASCADE)
    ADD_DATE = models.DateTimeField() #creation of record in db

    AscentTimeOut = models.IntegerField("Ascent time-out (Minutes) Mta",blank=True, null=True)
    BuoyancyNudge = models.IntegerField("Ascent buoyancy nudge (Counts) Mbn",blank=True, null=True)
    BuoyancyNudgeInitial = models.IntegerField("Initial buoyancy nudge (Counts) Mbi",blank=True, null=True)
    ConnectTimeOut = models.IntegerField("Host-connect time-out (Seconds) Mht",blank=True, null=True)
    CpActivationP = models.IntegerField("Continuous profile activation (Decibars) Mc",blank=True, null=True)
    DeepProfileDescentTime = models.IntegerField("Deep-profile descent time (Minutes) Mtj",blank=True, null=True)
    DeepProfileBuoyancyPos = models.IntegerField("Deep-profile buoyancy position (Counts) Mbj",blank=True, null=True)
    DeepProfilePressure = models.IntegerField("Deep-profile pressure (Decibars) Mj",blank=True, null=True)
    DownTime = models.IntegerField("Down time (Minutes) Mtd", blank=True, null=True)
    FullExtension = models.IntegerField("Buoyancy full extension (Counts) Mff",blank=True, null=True)
    FullRetraction = models.IntegerField("Buoyancy full retraction (Counts) Mfr",blank=True, null=True)
    IceDetectionP = models.FloatField("Ice detection: Mixed-layer Pmax (Decibars) Mix",blank=True, null=True)
    IceEvasionP = models.FloatField("Ice detection: Mixed-layer Pmin (Decibars) Min",blank=True, null=True)
    IceMLTCritical = models.FloatField("Ice detection: Mixed-layer Tcritical (C) Mit",blank=True, null=True)
    IceMonths = models.CharField("Ice detection: Winter months [DNOSAJJMAMFJ] Mib",max_length=25, blank=True, null=True)
    IsusInit = models.IntegerField(blank=True, null=True)
    HpvEmfK = models.FloatField("HPV b-EMF coefficient (Volt-Sec/Rad) Mfk",blank=True, null=True)
    HpvRes = models.IntegerField("HPV winding resistance (Ohms) Mfw",blank=True, null=True)
    MaxAirBladder = models.IntegerField("Maximum air bladder pressure (Counts) Mfb",blank=True, null=True)
    MaxLogKb = models.IntegerField(blank=True, null=True)
    MissionPrelude = models.IntegerField("Mission prelude (Minutes) Mtp", blank=True, null=True)
    OkVacuum = models.IntegerField("OK vacuum threshold (Counts) Mfv",blank=True, null=True)
    PActivationBuoyancyPosition = models.IntegerField("P-Activation buoyancy position (Counts) Mfs",blank=True, null=True)
    ParkDescentTime = models.IntegerField("Park descent time (Minutes) Mtk",blank=True, null=True)
    ParkBuoyancyPos = models.IntegerField("Park buoyancy position (Counts) Mbp",blank=True, null=True)
    ParkPressure = models.IntegerField("Park pressure (Decibars) Mk", blank=True, null=True)
    PnPCycleLen = models.IntegerField("Park-n-profile cycle length Mn",blank=True, null=True)
    TelemetryRetry = models.IntegerField("Telemetry retry interval (Minutes) Mhr",blank=True, null=True)
    TimeOfDay = models.IntegerField("ToD for down-time expiration (Minutes) Mtc", blank=True, null=True)
    UpTime = models.IntegerField("Up time (Minutes) Mtu",blank=True, null=True)
    PhBattMode = models.IntegerField(blank=True, null=True)
    Verbosity = models.IntegerField("Logging verbosity [0-5] D",blank=True, null=True)
    DebugBits = models.CharField("DebugBits D",max_length=25, blank=True, null=True)
    MissionSignature = models.CharField("Mission signature (hex)",max_length=25, blank=True, null=True)

    COMMENTS = models.TextField(blank=True, null=True)

    #For admin detail view
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    #Default return
    def __str__(self): 
        return str(self.DEPLOYMENT)