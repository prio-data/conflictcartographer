# Generated by Django 2.2.6 on 2019-11-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='opened',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='registered',
            field=models.BooleanField(default=False),
        ),
    ]
