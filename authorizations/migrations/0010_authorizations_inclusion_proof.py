# Generated by Django 3.2.7 on 2021-10-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorizations', '0009_alter_authorizations_start_validity'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorizations',
            name='inclusion_proof',
            field=models.TextField(default='Inclusion proof not available'),
            preserve_default=False,
        ),
    ]