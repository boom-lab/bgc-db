from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .serializers import SensorSerializer
from .models import sensor

#test
import csv
from django.http import HttpResponse

def sensors_csv(request):

    # Get all data from UserDetail Databse Table
    sensors = sensor.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensors_{}.txt"'.format(datetime.now().strftime("%Y_%m_%d"))

    writer = csv.writer(response)
    writer.writerow(['SENSOR', 'SENSOR_MAKER', 'SENSOR_MODEL', 'SENSOR_SERIAL_NO'])

    for record in sensors:
        writer.writerow([record.SENSOR, record.SENSOR_MAKER, record.SENSOR_MODEL, record.SENSOR_SERIAL_NO])
    return response

# API, get single sensor record
class GetSensor(APIView):
 
    def get(self, request, pk=2):
        dog = get_object_or_404(sensor, pk=pk)

        serializer = SensorSerializer(dog)
        return Response(serializer.data, status=status.HTTP_200_OK)