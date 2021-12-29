# Generated by Django 2.2.24 on 2021-12-21 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_M_', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=200)),
                ('departure_time', models.DateField()),
                ('startpoint', models.CharField(max_length=300)),
                ('endpoint', models.CharField(max_length=300)),
                ('number_seats', models.IntegerField(max_length=100)),
            ],
        ),
    ]