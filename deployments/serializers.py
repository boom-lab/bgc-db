from rest_framework import serializers 
from .models import deployment
from missions.serializers import MissionSerializer
from missions.models import mission
from sensors.serializers import SensorSerializer
from sensors.models import sensor

#API
class DeploymentSerializer(serializers.ModelSerializer):
    missions = MissionSerializer(many=True)
    sensors = SensorSerializer(many=True)

    class Meta:
        model = deployment

        fields = [field.name for field in deployment._meta.fields]
        fields.extend(['missions','sensors'])

    def create(self, validated_data):
        missions_data = validated_data.pop('missions')
        sensors_data = validated_data.pop('sensors')
        deployment_ob = deployment.objects.create(**validated_data)

        for mission_data in missions_data:
            mission.objects.create(DEPLOYMENT=deployment_ob, **mission_data)

        for sensor_data in sensors_data:
            sensor.objects.create(DEPLOYMENT=deployment_ob, **sensor_data)

        return deployment_ob