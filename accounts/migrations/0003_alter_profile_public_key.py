# Generated by Django 3.2.5 on 2021-07-21 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_public_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_key',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]