# Generated by Django 4.2.4 on 2023-08-15 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opanahub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
