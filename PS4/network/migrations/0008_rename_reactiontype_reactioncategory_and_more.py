# Generated by Django 4.1 on 2022-11-08 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_reaction'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReactionType',
            new_name='ReactionCategory',
        ),
        migrations.RenameField(
            model_name='reaction',
            old_name='type',
            new_name='category',
        ),
    ]
