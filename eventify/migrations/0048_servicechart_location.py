# Generated by Django 2.2.1 on 2022-05-22 17:14

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0047_auto_20220522_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicechart',
            name='location',
            field=location_field.models.plain.PlainLocationField(default='41.088165, 29.043431', max_length=63),
        ),
    ]