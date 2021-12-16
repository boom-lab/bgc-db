from django.core.management.base import BaseCommand
from choices.models import deployment_platforms_C17

#Custom command to add vocabularies from csv
#To run:
#python manage.py activate_ships

class Command(BaseCommand):

    def handle(self, **options):

        ships = ["Volendam"]

        dplatforms = deployment_platforms_C17.objects.filter(VALUE__in=ships)

        for ship in dplatforms:
            ship.ACTIVE=True
            ship.save()