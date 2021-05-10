from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.http import HttpResponse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view#, permission_classes

from .models import deployment
from .serializers import DeploymentSerializer, CurrentDeploymentSerializer
import json


#Admin area
def admin_detail_view(request, admin_site, entry_id):
    entry = get_object_or_404(deployment, pk=entry_id)
    missions = entry.missions.all()
    
    context = dict(
        # Include common variables for rendering the admin template.
        admin_site.each_context(request),
        opts=deployment._meta,
        # Data for detail list
        entry=entry,
        entry_id=entry_id,
        missions=missions
    )
    return render(request, 'admin/detail_view.html', context)

def export_metadata(request, entry_id):

    #Get data from deployment, sensor, and mission tables
    d = get_object_or_404(deployment, pk=entry_id)
    sensors = d.sensors.all()

    file_loader = FileSystemLoader('templates') # directory of template file
    env = Environment(loader=file_loader)

    template = env.get_template('BGC_metadata.html') # load template file

    #Convert decimal degrees to degrees decimal minutes
    if d.LAUNCH_LATITUDE:
        lat_degrees = int(d.LAUNCH_LATITUDE)
        lat_min = (d.LAUNCH_LATITUDE - lat_degrees)*60

        long_degrees = int(d.LAUNCH_LONGITUDE)
        long_min = (d.LAUNCH_LONGITUDE - long_degrees)*60

        d.LAUNCH_POSITION = str(lat_degrees) +" "+ str(round(lat_min,6)) +" "+ str(long_degrees) +" "+ str(round(long_min,6))
    else:
        d.LAUNCH_POSITION ='99 99 999 99'

    if d.START_DATE:
        d.START_DATE = d.START_DATE.strftime('%d %m %Y %H %M')
    else:
        d.START_DATE = '99 99 9999 99 99'

    if d.LAUNCH_DATE:
        d.LAUNCH_DATE = d.LAUNCH_DATE.strftime('%d %m %Y %H %M')
    else:
        d.LAUNCH_DATE = '99 99 9999 99 99'

    if not d.IRIDIUM_PROGRAM_NO:
        d.IRIDIUM_PROGRAM_NO = 'n/a'

    if not d.DEPLOYMENT_REFERENCE_STATION_ID:
        d.DEPLOYMENT_REFERENCE_STATION_ID = 'n/a'

    if not d.CUSTOMIZATION:
        d.CUSTOMIZATION = 'n/a'

    if not d.COMMENTS:
        d.COMMENTS = 'n/a'
        
    nitrate_coefs = []
    for s in sensors:
        if s.SENSOR_CALIB_DATE:
            s.SENSOR_CALIB_DATE = s.SENSOR_CALIB_DATE.strftime('%d %m %Y')
        else:
            s.SENSOR_CALIB_DATE = 'n/a'

        if s.SENSOR_MAKER:
            aoml_maker_translator = {
                'WETLABS':'WetLabs Inc',
            }
            try:
                s.SENSOR_MAKER = aoml_maker_translator[s.SENSOR_MAKER]
            except:
                pass

        s.PREDEPLOYMENT_CALIB_COEFFICIENT = json.dumps(s.PREDEPLOYMENT_CALIB_COEFFICIENT).replace('"','').strip('{}').replace(':','=').replace(' ','').replace(',',';')

    #Render with jinja template
    output = template.render(d=d, sensors=sensors)

    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_{}.meta"'.format(d.AOML_ID, str(d.FLOAT_SERIAL_NO))
    return response

#APIs
#Add metadata, get metadata
class MetadataView(generics.ListCreateAPIView): #Read and write only
    permission_classes=[IsAuthenticated]
    serializer_class=DeploymentSerializer
    queryset=deployment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in deployment._meta.fields]

#Current metadata api, only most recent mission record (all sensors)
class GetCrtMetadata(generics.ListAPIView): #Read only
    serializer_class = CurrentDeploymentSerializer
    queryset=deployment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in deployment._meta.fields]



#Get WMO# by serial number
#No token needed
@api_view(['GET'])
def get_wmo(request):
    filters={}
    try:
        filters['FLOAT_SERIAL_NO'] = request.GET['FLOAT_SERIAL_NO']
    except:
        return JsonResponse({'details':'Error: FLOAT_SERIAL_NO not provided'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        filters['PLATFORM_TYPE'] = request.GET['PLATFORM_TYPE']
    except:
        return JsonResponse({'details':'Error: PLATFORM_TYPE not provided'}, status=status.HTTP_400_BAD_REQUEST)

    queryset = deployment.objects.filter(**filters)

    if len(queryset)==0:
        return JsonResponse({'details':'Error: no float found'}, status=status.HTTP_400_BAD_REQUEST)
    if len(queryset)>1:
        return JsonResponse({'details':'Error: multiple floats selected'}, status=status.HTTP_400_BAD_REQUEST)

    deployment_entry = queryset.first()
    return JsonResponse({
        'PLATFORM_TYPE':str(deployment_entry.PLATFORM_TYPE),
        'FLOAT_SERIAL_NO':deployment_entry.FLOAT_SERIAL_NO,
        'WMO':deployment_entry.PLATFORM_NUMBER,
    })

@api_view(['GET'])
def get_cal(request):
    filters = {}
    
    #Get parameters
    PLATFORM_NUMBER = request.GET.get('PLATFORM_NUMBER', None)
    if PLATFORM_NUMBER:
        filters['PLATFORM_NUMBER'] = PLATFORM_NUMBER

    FLOAT_SERIAL_NO = request.GET.get('FLOAT_SERIAL_NO', None)
    if FLOAT_SERIAL_NO:
        filters['FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO

    PLATFORM_TYPE = request.GET.get('PLATFORM_TYPE', None)
    if PLATFORM_TYPE:
        filters['PLATFORM_TYPE'] = PLATFORM_TYPE

    queryset = deployment.objects.filter(**filters)

    #Error handling
    if not PLATFORM_NUMBER and not FLOAT_SERIAL_NO and not PLATFORM_TYPE:
        return JsonResponse({'details':'Error: WMO must be specified, or FLOAT_SERIAL_NO and PLATFORM_TYPE'}, 
        status=status.HTTP_400_BAD_REQUEST) 
    if not PLATFORM_NUMBER:
        if not FLOAT_SERIAL_NO or not PLATFORM_TYPE:
            return JsonResponse({'details':'Error: both FLOAT_SERIAL_NO and PLATFORM_TYPE must be specified, or WMO'}, status=status.HTTP_400_BAD_REQUEST) 
    if len(queryset)>1:
        return JsonResponse({'details':'Error: multiple floats selected'}, status=status.HTTP_400_BAD_REQUEST)

    deployment_entry = queryset.first()
    sensors = deployment_entry.sensors.all() #Get sensors of this query

    result = {}
    for sensor in sensors:
        result[str(sensor.SENSOR)] = {
            "SENSOR_MAKER":sensor.SENSOR_MAKER.VALUE,
            "SENSOR_MODEL":sensor.SENSOR_MODEL.VALUE,
            "SENSOR_SERIAL_NO":sensor.SENSOR_SERIAL_NO,
            "SENSOR_CALIB_DATE":sensor.SENSOR_CALIB_DATE,
            "COMMENTS":sensor.COMMENTS,
            "PREDEPLOYMENT_CALIB_EQUATION":sensor.PREDEPLOYMENT_CALIB_EQUATION,
            "PREDEPLOYMENT_CALIB_COEFFICIENT":sensor.PREDEPLOYMENT_CALIB_COEFFICIENT
        }

    return JsonResponse(result)

@api_view(['GET'])
def get_locations(request):
    filters = {}
    
    #Get parameters
    PLATFORM_NUMBER = request.GET.get('PLATFORM_NUMBER', None)
    if PLATFORM_NUMBER:
        filters['PLATFORM_NUMBER'] = PLATFORM_NUMBER
    else:
        return JsonResponse({'details':'Error: PLATFORM_NUMBER (WMO) must be specified'}, 
        status=status.HTTP_400_BAD_REQUEST) 


    queryset = deployment.objects.filter(**filters)

    deployment_entry = queryset.first()
    cycle_metadata = deployment_entry.cycle_metadata.all() #Get cycle data for this query

    results = {
        "GpsFixDate":list(cycle_metadata.values_list('GpsFixDate', flat=True)),
        "GpsLat":list(cycle_metadata.values_list('GpsLat', flat=True)),
        "GpsLong":list(cycle_metadata.values_list('GpsLong', flat=True))
    }

    return JsonResponse(results)