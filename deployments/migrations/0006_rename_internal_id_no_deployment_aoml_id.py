# Generated by Django 3.2 on 2021-04-16 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0005_rename_add_dated_deployment_add_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deployment',
            old_name='INTERNAL_ID_NO',
            new_name='AOML_ID',
        ),
    ]
