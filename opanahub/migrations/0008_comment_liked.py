# Generated by Django 4.2.4 on 2023-08-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opanahub', '0007_posts_sav'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='liked',
            field=models.BooleanField(default=False),
        ),
    ]
