from pyexpat import model
from rest_framework import serializers

from logs.serializers import DeploymentTrackingSerializer 
from .models import deployment
from missions.serializers import AddMissionSerializer, MissionSerializer
from sensors.serializers import AddSensorSerializer, SensorSerializer
from missions.models import mission
from sensors.models import sensor

#Fields from deployment table with nested sensor data
class DeploymentMetaSerializer(serializers.ModelSerializer):

    #Reformat
    DEPLOYMENT_PLATFORM = serializers.CharField(source="DEPLOYMENT_PLATFORM.VALUE", allow_null=True)
    LAUNCH_DATE = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_report = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    next_report = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    age = serializers.IntegerField(source="age.days", allow_null=True)
    last_event = serializers.CharField(source="last_event.EVENT", allow_null=True)
    comment = serializers.CharField(source="last_event.COMMENT", allow_null=True)

    class Meta:
        model = deployment

        fields = [field.name for field in deployment._meta.fields if field.name not in ['IMEI', 'SIM']]
        fields.extend(['sensors','last_report','days_since_last','next_report','last_event','last_cycle','last_location','comment','status','age',
        'incoming_status','internal_inspection_status','pressure_test_status','docktest_status','flow_through_status'])
        read_only_fields = fields

    def __init__(self, *args, **kwargs): #For gettting request to results column filter of sensor data
        super(DeploymentMetaSerializer, self).__init__(*args, **kwargs)
        self.fields['sensors'] = SensorSerForDeployment(many=True, context=self.context)

        #Filters which fields are returned
        fields = self.context['request'].query_params.get('deployment_fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
     
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

#Posting and updating metadata
class PostUpdateSerializer(serializers.ModelSerializer):
    #
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

class SensorSerForDeployment(serializers.ModelSerializer):
    class Meta:
        model = sensor
        fields = [field.name for field in sensor._meta.fields]

    #Filters which fields are returned
    def __init__(self, *args, **kwargs):
        super(SensorSerForDeployment, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('sensor_fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `sensor_fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)



class TrackingSerializer(serializers.ModelSerializer):
    deployment_tracking = DeploymentTrackingSerializer(many=True)
    class Meta:
        model = deployment
        fields = ("FLOAT_SERIAL_NO", "deployment_tracking")






