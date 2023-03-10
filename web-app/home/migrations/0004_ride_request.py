# Generated by Django 4.1.5 on 2023-02-05 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_vehicle_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=150)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('numberOfPassenger', models.IntegerField(default=4)),
                ('canShare', models.BooleanField()),
            ],
        ),
    ]
