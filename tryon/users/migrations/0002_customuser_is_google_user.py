# Generated by Django 4.2.19 on 2025-02-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_google_user',
            field=models.BooleanField(default=False),
        ),
    ]
