from django.db import models
from .models import sensor_types, sensor_makers, sensor_models, instrument_types, platform_makers, platform_types, transmission_systems

def get_choices(desired_choices):

    if desired_choices == 'sensor_types':
        model = sensor_types
    elif desired_choices == 'sensor_makers':
        model = sensor_makers
    elif desired_choices == 'sensor_models':
        model = sensor_models
    elif desired_choices == 'instrument_types':
        model = instrument_types
    elif desired_choices == 'platform_makers':
        model = platform_makers
    elif desired_choices == 'platform_types':
        model = platform_types
    elif desired_choices == 'transmission_systems':
        model = transmission_systems

    choices = model.objects.filter(ACTIVE=True).all()

    entries = [(choice.VALUE, choice.DISPLAY) for choice in choices]
    
    return entries