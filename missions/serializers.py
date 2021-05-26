from rest_framework import serializers 
from .models import mission
 
 
class AddMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = mission
        exclude = ['DEPLOYMENT']

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = mission
        fields = '__all__'
