# Generated by Django 4.1 on 2022-11-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_reactioncategory_emoji'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reactioncategory',
            options={'verbose_name_plural': 'Reaction categories'},
        ),
        migrations.AddField(
            model_name='user',
            name='shadowbanned',
            field=models.BooleanField(default=False),
        ),
    ]