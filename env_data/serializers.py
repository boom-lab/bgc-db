from rest_framework import serializers 
from .models import continuous_profile, discrete_profile, park, cycle_metadata, mission_reported

class ConProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = continuous_profile
        fields = [field.name for field in continuous_profile._meta.fields].remove('DEPLOYMENT')
        #exclude = ['DEPLOYMENT']

class DisProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = discrete_profile
        fields = [field.name for field in discrete_profile._meta.fields].remove('DEPLOYMENT')
        #exclude = ['DEPLOYMENT']

class ParkSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = park
        fields = [field.name for field in park._meta.fields].remove('DEPLOYMENT')
        #exclude = ['DEPLOYMENT']

class CycleMetaSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = cycle_metadata
        fields = [field.name for field in cycle_metadata._meta.fields].remove('DEPLOYMENT')
        #exclude = ['DEPLOYMENT']

class MissionReportedSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = mission_reported
        fields = [field.name for field in mission_reported._meta.fields].remove('DEPLOYMENT')
        #exclude = ['DEPLOYMENT']