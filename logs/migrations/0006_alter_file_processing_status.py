# Generated by Django 3.2 on 2021-05-13 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0005_alter_file_processing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_processing',
            name='STATUS',
            field=models.CharField(choices=[('Success', 'Success'), ('Fail', 'Fail'), ('Skip', 'Skip'), ('Reprocess', 'Reprocess')], max_length=200),
        ),
    ]
