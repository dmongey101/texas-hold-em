# Generated by Django 2.0.8 on 2019-02-23 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='owner',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
