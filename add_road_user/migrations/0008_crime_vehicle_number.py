# Generated by Django 4.0.4 on 2022-06-03 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_road_user', '0007_offencelist_crime'),
    ]

    operations = [
        migrations.AddField(
            model_name='crime',
            name='vehicle_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
