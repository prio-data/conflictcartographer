# Generated by Django 3.1.2 on 2020-11-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201102_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='meta',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
