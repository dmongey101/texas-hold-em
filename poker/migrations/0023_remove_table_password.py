# Generated by Django 2.0.8 on 2019-02-21 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0022_table_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='password',
        ),
    ]