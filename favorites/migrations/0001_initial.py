# Generated by Django 4.1 on 2024-09-15 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('distance', models.FloatField()),
                ('cuisine', models.CharField(max_length=120)),
                ('rating', models.FloatField()),
                ('post_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite',
                'ordering': ['title'],
            },
        ),
    ]
