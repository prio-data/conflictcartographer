# Generated by Django 3.1.2 on 2020-11-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0021_auto_20201119_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='fulfilled',
            field=models.BooleanField(default=False, editable=False, help_text='Indicates whether or not the invitation has been fulfilled, meaning a user has been registered for it.'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='mailed',
            field=models.BooleanField(default=False, editable=False, help_text='Indicates whether or not the invitation has been dispatched, that is, if an email has been sent to the target recipient'),
        ),
    ]
