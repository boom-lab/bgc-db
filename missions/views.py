from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from jinja2 import Environment, FileSystemLoader

from .models import mission

#Create NAVIS mission config file
def export_NAVIS_mission_config(request, entry_id):
    """Tested with NAVIS_EBR float"""

    #Get data from mission
    m = get_object_or_404(mission, pk=entry_id)

    output = "Something\nTest"

    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_{}.meta"'.format('test', 'test')
    return response