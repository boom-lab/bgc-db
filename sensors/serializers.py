from rest_framework import serializers 
from .models import sensor
 
 
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = sensor
        fields = [field.name for field in sensor._meta.fields]


class AddSensorSerializer(serializers.ModelSerializer): 
    class Meta:
        model = sensor
        exclude = ['DEPLOYMENT']