# Generated by Django 3.2 on 2021-04-29 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_data', '0016_alter_cycle_metadata_parkobs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='continuous_profile',
            old_name='NB_SAMPLE_DOXY',
            new_name='NB_SAMPLE_OPTODE',
        ),
        migrations.AlterField(
            model_name='cycle_metadata',
            name='ParkDescentP',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
