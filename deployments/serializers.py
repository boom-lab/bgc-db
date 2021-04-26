from rest_framework import serializers 
from .models import deployment
from missions.serializers import MissionSerializer
from missions.models import mission
from sensors.serializers import SensorSerializer
from sensors.models import sensor

#API
class DeploymentSerializer(serializers.ModelSerializer):
    #Returns deployment with all mission records (and all sensor records)
    missions = MissionSerializer(many=True)
    sensors = SensorSerializer(many=True)

    class Meta:
        model = deployment

        fields = [field.name for field in deployment._meta.fields]
        fields.extend(['missions','sensors'])

    #Creating related records
    def create(self, validated_data):
        missions_data = validated_data.pop('missions')
        sensors_data = validated_data.pop('sensors')
        deployment_ob = deployment.objects.create(**validated_data)

        for mission_data in missions_data:
            mission.objects.create(DEPLOYMENT=deployment_ob, **mission_data)

        for sensor_data in sensors_data:
            sensor.objects.create(DEPLOYMENT=deployment_ob, **sensor_data)

        return deployment_ob

class CurrentDeploymentSerializer(serializers.ModelSerializer):
    #Returns deployment with only the most recent mission record (and all sensor records)
    #mission_entry = MissionSerializer(many=True)
    mission = serializers.SerializerMethodField(read_only=True)
    sensors = SensorSerializer(many=True)

    class Meta:
        model = deployment

        fields = [field.name for field in deployment._meta.fields]
        fields.extend(['mission','sensors'])

    def get_mission(self, obj):
        return MissionSerializer(instance=obj.missions.order_by('-ADD_DATE').first()).data
