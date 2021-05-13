from rest_framework import serializers 
from .models import continuous_profile, discrete_profile, park, cycle_metadata, mission_reported

class ConProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = continuous_profile
        fields = '__all__'

class DisProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = discrete_profile
        fields = '__all__'

class ParkSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = park
        fields = '__all__'

class CycleMetaSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = cycle_metadata
        fields = '__all__'


class MissionReportedSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = mission_reported
        fields = '__all__'