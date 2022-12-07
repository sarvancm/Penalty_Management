# Generated by Django 4.0.4 on 2022-06-03 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('add_road_user', '0006_alter_create_roaduser_mobile_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='OffenceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offence', models.CharField(max_length=100)),
                ('offence_fine', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty', models.IntegerField()),
                ('payment_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('offence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_road_user.offencelist')),
                ('offender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_road_user.create_roaduser')),
            ],
        ),
    ]