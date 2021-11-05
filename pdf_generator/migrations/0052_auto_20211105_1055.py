# Generated by Django 3.1 on 2021-11-05 10:55

from django.db import migrations


def fill_in_the_price_field(apps, schema_editor):
    Designation = apps.get_model('pdf_generator', 'Designation')
    HourlyRate = apps.get_model('pdf_generator', 'HourlyRate')
    for designation in Designation.objects.all():
        if designation.price is None or designation.price == '':
            designation.price = HourlyRate.objects.all().first()
            designation.save(update_fields=['price'])


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0051_auto_20211104_1531'),
    ]

    operations = [
        migrations.RunPython(fill_in_the_price_field),
    ]
