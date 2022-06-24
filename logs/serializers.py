from logs.models import deployment_tracking


from rest_framework import serializers 
from .models import deployment_tracking

class DeploymentTrackingSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = deployment_tracking
        fields = ("__all__")