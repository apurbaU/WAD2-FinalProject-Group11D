# Generated by Django 2.2.28 on 2023-03-22 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gutigers', '0002_auto_20230322_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
