# Generated by Django 3.1 on 2021-09-08 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0034_designation_hours_to_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='designation',
            name='hours_to_months',
        ),
        migrations.AddField(
            model_name='phase',
            name='hours_to_months',
            field=models.BooleanField(default=False, verbose_name='hours to months?'),
        ),
    ]
