# Generated by Django 4.1 on 2023-03-24 13:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='rating',
            field=models.IntegerField(default=100, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
