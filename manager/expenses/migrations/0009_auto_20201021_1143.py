# Generated by Django 3.1.1 on 2020-10-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0008_auto_20201016_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liquidation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processed', 'Processed'), ('Rejected', 'Rejected'), ('Updated', 'Updated')], default='Pending', max_length=30),
        ),
    ]
