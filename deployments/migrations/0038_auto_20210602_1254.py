# Generated by Django 3.2 on 2021-06-02 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0037_remove_deployment_deployment_platform_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='BATTERY_SERIAL_NO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='PUMP_BATTERY_SERIAL_NO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]