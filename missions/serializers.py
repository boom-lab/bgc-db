from rest_framework import serializers 
from .models import mission
 
 
class MissionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = mission
        #fields = [field.name for field in mission._meta.fields]
        exclude = ['DEPLOYMENT']

class AddMissionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = mission
        fields = "__all__"
