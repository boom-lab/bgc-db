# Generated by Django 3.2 on 2021-05-25 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0031_auto_20210525_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployment',
            name='DEPLOYMENT_TYPE',
        ),
    ]