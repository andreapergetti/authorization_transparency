# Generated by Django 3.2.5 on 2021-07-19 15:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authorizations', '0005_alter_authorizations_start_validity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorizations',
            name='start_validity',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
