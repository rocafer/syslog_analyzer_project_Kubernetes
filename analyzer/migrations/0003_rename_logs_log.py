# Generated by Django 4.0 on 2023-08-01 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0002_logs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Logs',
            new_name='Log',
        ),
    ]
