# Generated by Django 2.2.1 on 2022-01-02 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0030_auto_20220102_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isLate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='isLate',
            field=models.BooleanField(default=False),
        ),
    ]
