# Generated by Django 3.2 on 2021-06-10 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0024_auto_20210610_1526'),
        ('deployments', '0041_auto_20210610_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='PLATFORM_TYPE',
            field=models.ForeignKey(blank=True, limit_choices_to={'ACTIVE': True}, max_length=25, null=True, on_delete=django.db.models.deletion.PROTECT, to='choices.platform_types', to_field='VALUE'),
        ),
    ]
