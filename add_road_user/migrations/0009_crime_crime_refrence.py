# Generated by Django 4.0.4 on 2022-06-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_road_user', '0008_crime_vehicle_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='crime',
            name='crime_refrence',
            field=models.CharField(max_length=100, null=True),
        ),
    ]