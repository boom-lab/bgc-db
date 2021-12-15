from django.core.management.base import BaseCommand
from choices.models import deployment_platforms_C17, sensor_types, sensor_makers, sensor_models, platform_types_wmo, platform_makers, platform_types, transmission_systems
import pandas as pd

#Custom command to add vocabularies from csv
#To run:
#python manage.py add_from_vocab --add_list_of_your_choice

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--add_sensor_types', action='store_true')
        parser.add_argument('--add_sensor_models', action='store_true')
        parser.add_argument('--add_sensor_makers', action='store_true')
        parser.add_argument('--add_platform_types_wmo', action='store_true')
        parser.add_argument('--add_platform_makers', action='store_true')
        parser.add_argument('--add_platform_types', action='store_true')
        parser.add_argument('--add_transmission_systems', action='store_true')
        parser.add_argument('--add_deployment_platform', action='store_true')

    def handle(self, **options):

        if options['add_sensor_types']:
            R25 = pd.read_csv('choices/vocab/R25.csv')
            for index, row in R25.iterrows():
                print(index)
                stypes = sensor_types(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, SOURCE='Nerc R25')
                stypes.save()

        if options['add_sensor_makers']:
            R26 = pd.read_csv('choices/vocab/R26.csv')
            for index, row in R26.iterrows():
                print(index)
                smakers = sensor_makers(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, SOURCE='Nerc R26')
                smakers.save()
    
    
        if options['add_sensor_models']:
            R27 = pd.read_csv('choices/vocab/R27.csv')
            for index, row in R27.iterrows():
                print(index)
                smodels = sensor_models(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, SOURCE='Nerc R27')
                smodels.save()

        if options['add_platform_types_wmo']:
            R08 = pd.read_csv('choices/vocab/R08.csv')
            for index, row in R08.iterrows():
                print(index)
                itypes = platform_types_wmo(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, SOURCE='Nerc R08')
                itypes.save()

        if options['add_platform_makers']:
            R24 = pd.read_csv('choices/vocab/R24.csv')
            for index, row in R24.iterrows():
                print(index)
                itypes = platform_makers(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, SOURCE='Nerc R24')
                itypes.save()

        if options['add_platform_types']:
            R23 = pd.read_csv('choices/vocab/R23.csv')
            for index, row in R23.iterrows():
                print(index)
                itypes = platform_types(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, 
                    SOURCE='Nerc R23',KEY=row['Key'])
                itypes.save()

        if options['add_transmission_systems']:
            R10 = pd.read_csv('choices/vocab/R10.csv')
            for index, row in R10.iterrows():
                print(index)
                itypes = transmission_systems(VALUE=row['altLabel'], DISPLAY=row['prefLabel'], DESCRIPTION=row['Definition'], ACTIVE=False, SOURCE='Nerc R10')
                itypes.save()

        if options['add_deployment_platform']:
            C17 = pd.read_csv('choices/vocab/C17.csv')
            for index, row in C17.iterrows():
                print(index)
                itypes = deployment_platforms_C17(VALUE=row['VALUE'], ICES=row['ICES'], DESCRIPTION=row['DESCRIPTION'], ACTIVE=False, SOURCE='C17', TYPE=None)
                itypes.save()