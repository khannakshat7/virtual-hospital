# Generated by Django 3.0.4 on 2020-06-20 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth0login', '0005_auto_20200621_0240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='id',
            new_name='appointmentid',
        ),
    ]
