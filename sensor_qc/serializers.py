from django.forms import IntegerField
from rest_framework import serializers 
from .models import sensor_qc

#General serializer
class SensorQCserializer(serializers.ModelSerializer):
    SENSOR = serializers.CharField(source="SENSOR.SENSOR")
    ADD_DATE = serializers.DateTimeField(format="%Y-%M-%d")
    class Meta:
        model = sensor_qc
        fields = '__all__'

#For Sensor QC page
class SensorQCdataSerializer(serializers.Serializer):
    FLOAT_SERIAL_NO = serializers.IntegerField(source="SENSOR.DEPLOYMENT.FLOAT_SERIAL_NO")
    PLATFORM_NUMBER = serializers.IntegerField(source="SENSOR.DEPLOYMENT.PLATFORM_NUMBER")
    SENSOR = serializers.CharField(source="SENSOR.SENSOR")
    SENSOR_SERIAL_NO = serializers.CharField(source="SENSOR.SENSOR_SERIAL_NO")
    START_CYCLE = serializers.IntegerField()
    END_CYCLE = serializers.IntegerField()
    QC_LEVEL = serializers.IntegerField(source="QC_LEVEL.VALUE")
    PROBLEM = serializers.CharField()
