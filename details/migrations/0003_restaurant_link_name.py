# Generated by Django 5.1.1 on 2024-09-20 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0002_restaurant_place_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='link_name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
