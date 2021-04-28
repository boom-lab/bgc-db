# Generated by Django 3.2 on 2021-04-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0006_auto_20210419_1550'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='sensor',
            name='sensors_sensor_SENSOR_CHECKS',
        ),
        migrations.AlterField(
            model_name='sensor',
            name='SENSOR_MODEL',
            field=models.CharField(blank=True, choices=[('DRUCK_2900PSIA', 'DRUCK_2900PSIA'), ('SBE41CP_V3.0c', 'SBE41CP_V3.0c'), ('DURAFET', 'DURAFET'), ('MCOMS', 'MCOMS'), ('SBE63_V3.2.2', 'SBE63_V3.2.2'), ('SUNA_V2', 'SUNA_V2'), ('SBE41CP_V5.3.4', 'SBE41CP_V5.3.4')], max_length=25, null=True),
        ),
        migrations.AddConstraint(
            model_name='sensor',
            constraint=models.CheckConstraint(check=models.Q(('SENSOR__in', ['FLUOROMETER_CHLA', 'TRANSISTOR_PH', 'CTD_CNDC', 'CTD_PRES', 'CTD_TEMP', 'OPTODE_DOXY', 'SPECTROPHOTOMETER_NITRATE', 'FLUOROMETER_CDOM', 'RADIOMETER_PAR', 'BACKSCATTERINGMETER_BBP700', 'PUMP_VOLTAGE', 'CPU_VOLTAGE']), ('SENSOR_MAKER__in', ['JAC', 'WETLABS', 'SBE', 'MBARI', 'DRUCK', 'SATLANTIC']), ('SENSOR_MODEL__in', ['DRUCK_2900PSIA', 'SBE41CP_V3.0c', 'DURAFET', 'MCOMS', 'SBE63_V3.2.2', 'SUNA_V2', 'SBE41CP_V5.3.4'])), name='sensors_sensor_SENSOR_CHECKS'),
        ),
    ]