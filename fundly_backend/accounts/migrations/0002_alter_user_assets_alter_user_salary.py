# Generated by Django 4.2.21 on 2025-05-28 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='assets',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='salary',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
