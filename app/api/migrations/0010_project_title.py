# Generated by Django 3.1.2 on 2020-11-06 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='title',
            field=models.CharField(default='No title', max_length=128),
            preserve_default=False,
        ),
    ]
