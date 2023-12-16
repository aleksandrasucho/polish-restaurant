# Generated by Django 3.2.23 on 2023-12-16 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('number_of_seats', models.IntegerField()),
                ('capacity', models.IntegerField(choices=[(2, '2'), (4, '4'), (6, '6'), (8, '8')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('number_of_guests', models.IntegerField()),
                ('table', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]