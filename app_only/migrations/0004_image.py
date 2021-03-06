# Generated by Django 3.2.5 on 2021-09-14 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_only', '0003_auto_20210914_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_image', to='app_only.user')),
                ('upload_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sneaker_image', to='app_only.sneaker')),
            ],
        ),
    ]
