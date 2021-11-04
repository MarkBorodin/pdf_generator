# Generated by Django 3.1 on 2021-11-03 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0047_auto_20211103_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='payment_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='pdf_generator.paymentinformation'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='signature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='pdf_generator.signature'),
        ),
    ]
