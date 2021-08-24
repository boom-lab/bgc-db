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

    def __init__(self, *args, **kwargs): #For gettting request to results column filter of sensor data
        super(CycleMetaSerializer, self).__init__(*args, **kwargs)

        #Filters which fields are returned
        fields = self.context['request'].query_params.get('output_fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MissionReportedSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = mission_reported
        fields = '__all__'