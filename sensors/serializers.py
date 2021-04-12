from rest_framework import serializers 
from .models import sensor
 
 
class SensorSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = sensor
        fields = ["ADD_DATE", "SENSOR", "SENSOR_MAKER","SENSOR_MODEL",
        "SENSOR_SERIAL_NO","PREDEPLOYMENT_CALIB_EQUATION","PREDEPLOYMENT_CALIB_COEFFICIENT"]