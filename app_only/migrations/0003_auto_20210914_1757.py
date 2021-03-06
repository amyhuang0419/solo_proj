# Generated by Django 3.2.5 on 2021-09-14 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_only', '0002_rename_sneaker_sneaker_sneaker_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sneaker',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='sneaker',
            name='users_who_comment',
        ),
        migrations.AlterField(
            model_name='sneaker',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sneaker_posted', to='app_only.user'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to='app_only.user')),
                ('upload_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sneaker_comment', to='app_only.sneaker')),
            ],
        ),
    ]
