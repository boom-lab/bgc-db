from django.core.management.base import BaseCommand
from choices.models import deployment_platforms_C17, deployment_platforms
from deployments.models import deployment

#To run:
#python manage.py copy

class Command(BaseCommand):

    def handle(self, **options):

        ds = deployment.objects.all()

        for d in ds:
            d.DEPLOYMENT_PLATFORM_OLD = d.DEPLOYMENT_PLATFORM
            d.save()