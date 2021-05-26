from env_data.serializers import CycleMetaSerializer
from rest_framework import serializers 
from .models import deployment
from missions.serializers import AddMissionSerializer, MissionSerializer
from sensors.serializers import AddSensorSerializer, SensorSerializer
from missions.models import mission
from sensors.models import sensor

#API
class DeploymentSerializer(serializers.ModelSerializer):
    #Returns deployment with all mission records (and all sensor records)
    missions = AddMissionSerializer(many=True)
    sensors = AddSensorSerializer(many=True)

    class Meta:
        model = deployment
        fields = [field.name for field in deployment._meta.fields]
        fields.extend(['missions','sensors'])

    #Creating related records
    def create(self, validated_data):
        missions_data = validated_data.pop('missions')
        sensors_data = validated_data.pop('sensors')
        deployment_ob = deployment.objects.create(**validated_data)

        print(deployment_ob)

        for mission_data in missions_data:
            mission.objects.create(DEPLOYMENT=deployment_ob, **mission_data)

        for sensor_data in sensors_data:
            sensor.objects.create(DEPLOYMENT=deployment_ob, **sensor_data)

        return deployment_ob

class CurrentDeploymentSerializer(serializers.ModelSerializer):
    #Returns deployment with only the most recent mission record (and all sensor records), and most recent cycle metadata
    mission = serializers.SerializerMethodField(read_only=True)
    latest_cycle = serializers.SerializerMethodField(read_only=True)
    sensors = SensorSerializer(many=True)

    class Meta:
        model = deployment

        fields = [field.name for field in deployment._meta.fields]
        fields.extend(['status','last_report','next_report','age','mission','sensors','latest_cycle'])

    def get_mission(self, obj):
        return MissionSerializer(instance=obj.missions.order_by('-ADD_DATE').first()).data

    def get_latest_cycle(self, obj):
        return CycleMetaSerializer(instance=obj.cycle_metadata.order_by('-GpsFixDate').first()).data