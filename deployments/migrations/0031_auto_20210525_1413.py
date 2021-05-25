# Generated by Django 3.2 on 2021-05-25 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0014_auto_20210525_1402'),
        ('deployments', '0030_alter_deployment_inst_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='BATTERY_MANUFACTURER',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.battery_manufacturers', to_field='VALUE'),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='BATTERY_TYPE',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.battery_types', to_field='VALUE'),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='DEPLOYMENT_PLATFORM',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.deployment_platforms', to_field='VALUE'),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='INST_TYPE',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.instrument_types_aoml', to_field='VALUE'),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='ORIGIN_COUNTRY',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.origin_countries', to_field='VALUE'),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='WMO_RECORDER_TYPE',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.wmo_recorder_types', to_field='VALUE'),
        ),
    ]
