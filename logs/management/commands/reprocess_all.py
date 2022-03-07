from django.core.management.base import BaseCommand
from logs.models import file_processing

#To run:
#python manage.py reprocess_all

class Command(BaseCommand):

    def handle(self, **options):

        pl = file_processing.objects.all()

        for p in pl:
            p.STATUS = 'Reprocess'
            p.save()