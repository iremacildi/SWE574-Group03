# Generated by Django 2.2.1 on 2021-11-30 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0019_auto_20211129_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerevent',
            name='approved_register',
            field=models.BooleanField(default=True),
        ),
    ]