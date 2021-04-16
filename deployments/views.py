from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.http import HttpResponse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view#, permission_classes

from .models import deployment
from .serializers import DeploymentSerializer, CurrentDeploymentSerializer


#Admin area
def admin_detail_view(request, admin_site, entry_id):
    entry = get_object_or_404(deployment, pk=entry_id)

    context = dict(
        # Include common variables for rendering the admin template.
        admin_site.each_context(request),
        opts=deployment._meta,
        # Data for detail list
        entry=entry,
        entry_id=entry_id
    )
    return render(request, 'admin/detail_view.html', context)

def export_metadata(request, entry_id):

    #Get data from deployment, sensor, and mission tables
    deployments = get_object_or_404(deployment, pk=entry_id)
    sensors = deployments.sensors.all()
    mission = deployments.missions.order_by('-ADD_DATE').first() #Only most recent mission record

    file_loader = FileSystemLoader('templates') # directory of template file
    env = Environment(loader=file_loader)

    template = env.get_template('BGC_metadata.html') # load template file

    output = template.render(d=deployments, sensors=sensors, mission=mission)

    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aoml_metadata_{}.txt"'.format(datetime.now().strftime("%Y_%m_%d"))
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
    permission_classes=[IsAuthenticated]
    serializer_class = CurrentDeploymentSerializer
    queryset=deployment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in deployment._meta.fields]

#No token needed
@api_view(['GET'])
def get_wmo(request):
    serial_number = request.GET['serial_number']

    deployment_entry = deployment.objects.filter(FLOAT_SERIAL_NO__exact=serial_number).first()
    print(deployment_entry)
    return JsonResponse({
        'FLOAT_SERIAL_NO':deployment_entry.FLOAT_SERIAL_NO,
        'WMO':deployment_entry.FLOAT_SERIAL_NO,
    })
