# Generated by Django 2.2.1 on 2022-01-01 20:55

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211203_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=location_field.models.plain.PlainLocationField(default='41.088165, 29.043431', max_length=63),
        ),
    ]