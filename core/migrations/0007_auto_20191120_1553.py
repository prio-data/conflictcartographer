# Generated by Django 2.2.6 on 2019-11-20 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20191120_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='cohort',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='core.Cohort'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitation', to=settings.AUTH_USER_MODEL),
        ),
    ]
