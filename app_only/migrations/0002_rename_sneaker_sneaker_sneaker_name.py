# Generated by Django 3.2.5 on 2021-09-13 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_only', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sneaker',
            old_name='sneaker',
            new_name='sneaker_name',
        ),
    ]
