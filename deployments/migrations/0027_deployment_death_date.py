# Generated by Django 3.2 on 2021-05-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0026_rename_lbt_serial_no_deployment_modem_serial_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='DEATH_DATE',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]