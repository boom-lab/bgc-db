from django.shortcuts import render
from .models import deployment
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import DeploymentSerializer
from django.http import HttpResponse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

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

#API
@api_view(['GET', 'POST'])
def deployment_view(request):
    if request.method == 'POST':
        deployment_data = JSONParser().parse(request)
        deployment_serializer = DeploymentSerializer(data=deployment_data)
        if deployment_serializer.is_valid():
            print('valid')
            deployment_serializer.save()
            return JsonResponse(deployment_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(deployment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None
    # elif request.method == 'GET':
    #     tutorials = Tutorial.objects.all()
        
    #     title = request.query_params.get('title', None)
    #     if title is not None:
    #         tutorials = tutorials.filter(title__icontains=title)
        
    #     tutorials_serializer = TutorialSerializer(tutorials, many=True)
    #     return JsonResponse(tutorials_serializer.data, safe=False)
    #     # 'safe=False' for objects serialization
 
    # elif request.method == 'DELETE':
    #     count = Tutorial.objects.all().delete()
    #     return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
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
    response['Content-Disposition'] = 'attachment; filename="sensors_{}.txt"'.format(datetime.now().strftime("%Y_%m_%d"))
    return response