# Generated by Django 3.2.9 on 2022-06-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpost',
            name='category',
            field=models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('cinema', 'Cinema'), ('fashion', 'fashion')], default='Art', max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='category',
            field=models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('cinema', 'Cinema'), ('fashion', 'fashion')], default='Art', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('cinema', 'Cinema'), ('fashion', 'fashion')], default='Art', max_length=20),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('cinema', 'Cinema'), ('fashion', 'fashion')], default='Art', max_length=20),
        ),
    ]
