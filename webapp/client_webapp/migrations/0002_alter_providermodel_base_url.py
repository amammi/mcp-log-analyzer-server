# Generated by Django 5.2.4 on 2025-07-05 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providermodel',
            name='base_url',
            field=models.URLField(default=None, null=True),
        ),
    ]
