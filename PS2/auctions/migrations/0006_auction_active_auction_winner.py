# Generated by Django 4.1 on 2022-09-22 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winners', to=settings.AUTH_USER_MODEL),
        ),
    ]
