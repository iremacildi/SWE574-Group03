# Generated by Django 2.2.1 on 2022-05-04 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0041_service_iscancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='currentAtt',
            field=models.IntegerField(default=0),
        ),
    ]
