# Generated by Django 3.2 on 2021-06-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0042_deployment_platform_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='CYCLES_FOR_DRIFT_PRES',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deployment',
            name='CYCLES_FOR_PROFILE_PRES',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deployment',
            name='NOMINAL_DRIFT_PRES',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deployment',
            name='NOMINAL_PROFILE_PRES',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deployment',
            name='PROFILE_SAMPLING_METHOD',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]