from rest_framework import serializers 
from .models import mission
 
 
class MissionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = mission
        fields = ['ADD_DATE']
