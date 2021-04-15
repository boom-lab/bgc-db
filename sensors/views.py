from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SensorSerializer
from .models import sensor

class GetSensors(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = SensorSerializer
    queryset=sensor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['ADD_DATE','SENSOR','SENSOR_MAKER','SENSOR_MODEL','SENSOR_SERIAL_NO','SENSOR_CALIB_DATE']