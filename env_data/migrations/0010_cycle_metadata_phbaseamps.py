# Generated by Django 3.2 on 2021-04-29 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_data', '0009_cycle_metadata_parkobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle_metadata',
            name='pHBaseAmps',
            field=models.FloatField(blank=True, null=True),
        ),
    ]