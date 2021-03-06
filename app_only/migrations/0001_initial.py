# Generated by Django 3.2.5 on 2021-09-13 13:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('birthdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sneaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sneaker', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('sku_number', models.CharField(max_length=255)),
                ('release_price', models.IntegerField()),
                ('release_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('sneaker_size', models.FloatField()),
                ('buy_price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sneakers_posted', to='app_only.user')),
                ('users_who_comment', models.ManyToManyField(related_name='commented_sneakers', to='app_only.User')),
                ('users_who_like', models.ManyToManyField(related_name='liked_sneakers', to='app_only.User')),
            ],
        ),
    ]
