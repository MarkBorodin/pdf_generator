# Generated by Django 3.1 on 2021-04-06 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0017_offerconfirmation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offerconfirmation',
            old_name='paid',
            new_name='signed',
        ),
    ]
