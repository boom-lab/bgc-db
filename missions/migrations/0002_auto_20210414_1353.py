# Generated by Django 3.2 on 2021-04-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='AscentTimeOut',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='BuoyancyNudge',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='BuoyancyNudgeInitial',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='ConnectTimeOut',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='CpActivationP',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='DebugBits',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='DeepProfileBuoyancyPos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='DeepProfileDescentTime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='DeepProfilePressure',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='DownTime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='FloatId',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='FullExtension',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='FullRetraction',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='HpvEmfK',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='HpvRes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='IceDetectionP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='IceEvasionP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='IceMLTCritical',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='IceMonths',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='IsusInit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='MaxAirBladder',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='MaxLogKb',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='MissionPrelude',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='OkVacuum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='PActivationBuoyancyPosition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='ParkBuoyancyPos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='ParkDescentTime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='ParkPressure',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='PhBattMode',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='PnPCycleLen',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='TelemetryRetry',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='TimeOfDay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='UpTime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='Verbosity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]