# Generated by Django 3.2 on 2021-12-16 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0057_alter_deployment_deployment_platform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployment',
            name='DEPLOYMENT_PLATFORM_OLD',
        ),
    ]