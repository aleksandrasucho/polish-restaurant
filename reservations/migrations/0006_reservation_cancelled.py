# Generated by Django 3.2.23 on 2024-01-09 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_alter_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]