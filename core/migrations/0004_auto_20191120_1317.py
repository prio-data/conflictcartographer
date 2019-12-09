# Generated by Django 2.2.6 on 2019-11-20 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '__first__'),
        ('core', '0003_mock'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='email',
            field=models.EmailField(default='pglandsverk@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invitation',
            name='projects',
            field=models.ManyToManyField(related_name='projects', to='api.Project'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='reached',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invitation',
            name='refkey',
            field=models.CharField(default=1111, max_length=32),
            preserve_default=False,
        ),
    ]