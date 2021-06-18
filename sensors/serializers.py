from rest_framework import serializers 
from .models import sensor, deployment

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
     
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        #print(self)
        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = sensor
        fields = [field.name for field in sensor._meta.fields]

class AddSensorSerializer(serializers.ModelSerializer): 
    class Meta:
        model = sensor
        exclude = ['DEPLOYMENT']


#For use in the SensorMetaSerializer
class DeploymentSerForSensor(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = deployment
        fields = [field.name for field in deployment._meta.fields]
        fields.remove('ADD_DATE')
        fields.remove('id')

class SensorMetaSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
    class Meta:
        model = sensor
        fields = [field.name for field in sensor._meta.fields]
        fields.extend(['DEPLOYMENT'])

    def __init__(self, *args, **kwargs):
        super(SensorMetaSerializer, self).__init__(*args, **kwargs)
        self.fields['DEPLOYMENT'] = DeploymentSerForSensor(context=self.context, read_only=True)

    #flattens nested serializers, moves deployment metadata to same level as sensor data
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        deployment_representation = representation.pop('DEPLOYMENT')
        for key in deployment_representation:
            if key == "COMMENTS": #Rename deployments comment field
                representation["DEPLOYMENT_COMMENTS"] = deployment_representation[key]
            else:
                representation[key] = deployment_representation[key]

        return representation