# Generated by Django 2.0.8 on 2018-11-29 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poker', '0003_auto_20181129_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hand',
            name='current_user',
        ),
        migrations.AddField(
            model_name='table',
            name='current_player',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='current_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
